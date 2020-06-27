#!/usr/bin/python3

import requests
from flask import request, Response, Flask
from flask_redis import FlaskRedis

# EB looks for an 'application' callable by default.
application = Flask(__name__)
redis_client = FlaskRedis(application)

application.config.from_pyfile('config.py')


@application.route('/ping')
def ping(*args, **kwargs):
    print(application.config['REDIS_URL'])

    redis_client.get('potato')
    import ipdb
    ipdb.set_trace()
    return Response('pong', 200)


@application.route('/<path:url>', methods=["GET", "POST"])
def _proxy(*args, **kwargs):
    if request.headers['Proxy-Authentication'] != config.API_KEY:
        return Response('Missing auth', 401)
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
    application.debug = True
    application.run(threaded=False, processes=1, port=5000, host='0.0.0.0')
    #application.run(host='0.0.0.0', port=5000)
