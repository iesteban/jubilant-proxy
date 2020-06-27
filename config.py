"""
Config file
"""
import os

API_KEY = os.getenv('API_KEY', 'h4323hkjl3h2425kj4gg5f4hgf45df')
REDIS_URL = os.getenv('REDIS_URL', "redis://redis:6379/0")
