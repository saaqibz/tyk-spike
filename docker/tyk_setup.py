#! /home/alex/workspace/tyk-spike/flask/bin/python
import requests
import json, pdb

USER_DASHBOARD_KEY = '22b603a3357b4dc2434739d56ec13bc1'
DASHBOARD_URL = 'http://tyk.docker:3000/'
TYK_API_URL = 'http://tyk.docker:8080/tyk/'
tyk_auth_header = {
    'X-Tyk-Authorization': '352d20ee67be67f6340b4c0605b044b7',
    'Authorization': USER_DASHBOARD_KEY,
    'admin-auth': 12345
}

def create_api():
    add_url = DASHBOARD_URL + 'api/apis'
    with open('apis.json', 'r') as f:
        apis = json.load(f)
        for api in apis:
            resp = requests.post(add_url, json=json.dumps(api), headers=tyk_auth_header)
            print api['name'] + ": " + resp.text

def hot_reload():
    requests.get(TYK_API_URL + 'reload/group', headers=tyk_auth_header)

def run():
    create_api()
    hot_reload()

if __name__ == '__main__':
    run()