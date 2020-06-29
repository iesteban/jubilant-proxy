"""
Config file
"""
import os

HTTP_PORT = os.getenv('HTTP_PORT', 5000)
REDIS_URL = os.getenv('REDIS_URL', "redis://redis:6379/0")
JWT_SIGNING_KEY = 'a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4ebfb378e22ad39c2d01 d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf'
PROXY_UPSTREAM_URL = 'http://requestbin.net/r/10kmrd51/'
