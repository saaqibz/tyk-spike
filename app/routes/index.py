from app import app, db
import json, requests
import pdb
from flask import request
from app.models import user
import users

from datetime import timedelta
from flask import make_response, request, current_app, send_from_directory
from functools import update_wrapper

class APICONFIG():
    tyk_api_url = 'http://tyk.docker:8080/'
    tyk_api_key = '352d20ee67be67f6340b4c0605b044b7'
    app_id = '8e6221d930e7440e450656fa5d84ccf7'
    restricted_api_name = 'restricted'

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route('/')
def root():
    return app.send_static_file('index.html')

# app = Flask(__name__, static_folder='../static')
# app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return json.dumps({'error': 'Not found'}), 404

@app.route('/auth/')
def hello_world():
    return 'Hello World!'

@app.route('/auth/store_token')
def store_token():
    pdb.set_trace()
    print 'Request Values {0}'.format([v for v in request.values])
    return json.dumps({'status':'token received'})


##
# see: @app.route('/auth/createuser') in users.py
##


@app.route('/auth/login', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers='Content-Type')
def login():
    print 'login started'
    try:
        email = request.json["email"]
        password = request.json['password']
        entity = user.User.query.filter(user.User.email == email).first()
        if entity.password == password:
            url = APICONFIG.tyk_api_url + APICONFIG.restricted_api_name + '/tyk/oauth/authorize-client/'
            headers = {'x-tyk-authorization': APICONFIG.tyk_api_key}
            # key_rules should have fileds but policy will be overwritten by apply_policy_id flag
            params = {
                'response_type': 'token',
                'client_id': APICONFIG.app_id,
                'key_rules': '{"rate": 3, \
                                "per": 1, \
                                "expires": 0, \
                                "quota_max": 1000, \
                                "quota_renews": 1429804261, \
                                "quota_remaining": 1000, \
                                "quota_renewal_rate": 90000, \
                                "apply_policy_id": "Default"}'
            }
            r = requests.post(url, data=params, headers=headers)
            print r.text
            if r.status_code == 200:
                token = r.json()['access_token']
                users.add_token(email, 244, token)
                return json.dumps({'login': 'success', 'token': token})
            else:
                return r.text, r.status_code
    except Exception as e:
        pass
    return json.dumps({'error': 'Invalid Credentials'}), 401

@app.route('/auth/status', methods=['GET'])
def test():
    return json.dumps({'status': 'ready'}) + '\n'

def get_token(cid):
    pass
