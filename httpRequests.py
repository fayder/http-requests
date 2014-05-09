import requests
from requests.auth import HTTPBasicAuth

ENDPOINT = 'http://0.0.0.0:8080'


def makeGet(url):
    r = requests.get(url)
    assert r.status_code == 200


def makePost(url):
    r = requests.post(url)
    assert r.status_code == 201


def makePut(url):
    r = requests.put(url)
    assert r.status_code == 200


def makeDelete(url):
    r = requests.delete(url)
    assert r.status_code == 204


def makeAuthGet(url):
    r = requests.get(url, auth=HTTPBasicAuth('bruce', 'wayne'))
    assert r.status_code == 200


def webAuthPost(url):
    with open('README.md') as f:
        headers = {'content-type': 'text'}
        r = requests.post(
            url,
            auth=HTTPBasicAuth('bruce', 'wayne'),
            data=f,
            headers=headers)
    assert r.status_code == 201
