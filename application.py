#!/usr/bin/python3

import requests
import datetime
import pickle
from flask import request, Response, Flask
from flask_redis import FlaskRedis

# EB looks for an 'application' callable by default.
application = Flask(__name__)
application.config.from_pyfile('config.py')
redis_client = FlaskRedis(application)

START_TIME_KEY = 'start_time'
REQUESTS_COUNT_KEY = 'request_coung'


def start_server():
    redis_client.set(START_TIME_KEY, pickle.dumps(datetime.datetime.now()))
    redis_client.set(REQUESTS_COUNT_KEY, 0)


def post_request_hook():
    """ After request has been made:
            Increase requests counter
    """
    redis_client.incr(REQUESTS_COUNT_KEY)


@application.route('/status')
def ping(*args, **kwargs):
    start_time = pickle.loads(
        redis_client.get(START_TIME_KEY))
    uptime = datetime.datetime.now() - start_time
    uptime_seconds = str(int(uptime.total_seconds()))
    requests = redis_client.get(REQUESTS_COUNT_KEY)
    response_content = f"Uptime: {uptime_seconds} seconds <br><br>Requests count: {requests}"

    post_request_hook()
    return Response(response_content, 200)


@application.route('/<path:url>', methods=["GET", "POST"])
def _proxy(*args, **kwargs):
    resp = requests.request(
        method=request.method,
        url=request.url.replace(
            request.host_url, 'http://10.248.23.100:8080/'),
        headers={key: value for (key, value)
                 in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding',
                        'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    start_server()
    application.debug = True
    application.run(threaded=False, processes=5, port=5000, host='0.0.0.0')
    # application.run(host='0.0.0.0', port=5000)
