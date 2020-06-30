#!/usr/bin/python3

import datetime
import uuid
import pickle
import jwt
import requests
from flask import request, Response, Flask
from flask_redis import FlaskRedis

# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.config.from_pyfile('config.py')
redis_client = FlaskRedis(application)

START_TIME_KEY = 'start_time'
REQUESTS_COUNT_KEY = 'request_count'
JWT_HEADER = 'x-my-jwt'


def start_server():
    """ Hook starting cache values
    """
    redis_client.set(START_TIME_KEY, pickle.dumps(datetime.datetime.now()))
    redis_client.set(REQUESTS_COUNT_KEY, 0)


def post_request_hook():
    """ After request has been made:
            Increase requests counter
    """
    redis_client.incr(REQUESTS_COUNT_KEY)


@application.route('/status')
def status(*args, **kwargs):
    """ Status html page with number of requests and uptime
    """

    start_time = pickle.loads(
        redis_client.get(START_TIME_KEY))
    uptime = datetime.datetime.now() - start_time
    uptime_seconds = str(int(uptime.total_seconds()))
    num_requests = redis_client.get(REQUESTS_COUNT_KEY).decode()
    response_content = f"Uptime: {uptime_seconds} seconds <br><br>Requests count: {num_requests}"

    post_request_hook()
    return Response(response_content, 200)


def _get_jwt_token():
    """ Compute JWT token
    """
    now_timestamp = int(datetime.datetime.now().timestamp())
    jti = uuid.uuid4().hex
    payload = {"user": "username", "date": "todays date"}
    claims = {
        'iat': now_timestamp,
        'jti': jti,
        'payload': payload,
    }

    jwt_token = jwt.encode(
        claims, application.config['JWT_SIGNING_KEY'], algorithm='HS512')
    # Test with jwt.decode(encoded,  application.config['JWT_SIGNING_KIT'], algorithms='HS512')
    return jwt_token


@application.route('/<path:url>', methods=["GET", "POST"])
def proxy(*args, **kwargs):
    """ Proxy endpoint. The upstream is in config['PROXY_UPSTREAM_URL']
    """

    # Compute headers
    headers = {key: value for (key, value)
               in request.headers if key != 'Host'}
    headers[JWT_HEADER] = _get_jwt_token()

    # Perform request
    resp = requests.request(
        method=request.method,
        url=request.url.replace(
            request.host_url, application.config['PROXY_UPSTREAM_URL']),
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    # Filter some headers for the response
    excluded_headers = ['content-encoding',
                        'content-length', 'transfer-encoding', 'connection']
    resp_headers = [(name, value) for (name, value) in resp.raw.headers.items()
                    if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, resp_headers)
    post_request_hook()
    return response


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    start_server()
    application.debug = True
    application.run(
        # threaded=False,
        # processes=1,
        port=application.config['HTTP_PORT'],
        host='0.0.0.0')
