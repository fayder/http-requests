import web
import json
import re
import base64


def getResponse(status, message):
    return json.dumps({'status': status, 'message': message})


class Index:
    def GET(self):
        # TODO: return json with instructions
        response = json.dumps(
            {
                'status': 200,
                'message': 'This is a dummy web.py server.',
                'requests': [
                    {
                        'method': 'GET',
                        'endpoint': '/get',
                        'description': 'Simple GET Request'
                        },
                    {
                        'method': 'POST',
                        'endpoint': '/post',
                        'description': 'Simple POST Request'
                        }
                    ]})
        return response


class HttpHandler:
    def GET(self):
        web.header('Content-Type', 'application/json')
        return getResponse(web.ctx.status, 'Successful GET request')

    def POST(self):
        web.header('Content-Type', 'application/json')
        web.ctx.status = '201 Created'
        data = web.data()
        print(data)
        return getResponse(web.ctx.status, 'Successful POST request')

    def PUT(self):
        web.header('Content-Type', 'application/json')
        return getResponse(web.ctx.status, 'Successful PUT request')

    def DELETE(self):
        web.ctx.status = '204 No Content'


class AuthHttpHandler:
    def GET(self):
        auth = web.ctx.env.get('HTTP_AUTHORIZATION')
        allowed = (('bruce', 'wayne'), ('clark', 'kent'))

        authreq = False
        if auth is None:
            authreq = True
        else:
            auth = re.sub('^Basic ', '', auth)
            username, password = base64.decodestring(auth).split(':')
            if (username, password) in allowed:
                raise web.seeother('/authenticated')
            else:
                authreq = True
        if authreq:
            web.header('WWW-Authenticate', 'Basic realm="Auth example"')
            web.ctx.status = '401 Unauthorized'
            return '401 Unauthorized'

    # TODO def POST(self):
    def POST(self):
        auth = web.ctx.env.get('HTTP_AUTHORIZATION')
        allowed = (('bruce', 'wayne'), ('clark', 'kent'))
        authreq = False
        if auth is None:
            authreq = True
        else:
            auth = re.sub('^Basic ', '', auth)
            username, password = base64.decodestring(auth).split(':')
            if (username, password) in allowed:
                web.ctx.status = '201 Created'
                return getResponse(
                    web.ctx.status,
                    'Successful Auth PUT request')
            else:
                authreq = True
        if authreq:
            web.header('WWW-Authenticate', 'Basic realm="Auth example"')
            web.ctx.status = '401 Unauthorized'
            return '401 Unauthorized'


class Authenticated():
    def GET(self):
        web.header('Content-Type', 'application/json')
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            return getResponse(
                web.ctx.status,
                'Successful Basic Auth GET request')
        else:
            raise web.seeother('/auth')

if __name__ == "__main__":
    urls = ('/', 'Index',
            '/get/*', 'HttpHandler',
            '/post/*', 'HttpHandler',
            '/put/*', 'HttpHandler',
            '/delete/*', 'HttpHandler',
            '/auth', 'AuthHttpHandler',
            '/authenticated', 'Authenticated')
    app = web.application(urls, globals())
    app.run()
