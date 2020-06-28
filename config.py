"""
Config file
"""
import os

API_KEY = os.getenv('API_KEY', 'h4323hkjl3h2425kj4gg5f4hgf45df')
REDIS_URL = os.getenv('REDIS_URL', "redis://redis:6379/0")
JWT_SIGNING_KIT = 'a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4ebfb378e22ad39c2d01 d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf'
