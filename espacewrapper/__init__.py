# espacewrapper/__init__.py

import os
import requests

JWT_KEY = os.environ.get('KEY', None)

class APIKeyMissingError(Exception):
    pass

if JWT_KEY is None:
    raise APIKeyMissingError(
        "Need JWT Key to run. "
        "Run again with KEY=YOUR_KEY_HERE python main.py"
    )
    
session = requests.Session()
session.params = {}
session.params['api_key'] = JWT_KEY

from .api import API