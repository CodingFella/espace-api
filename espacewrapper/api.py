

from . import session
import os

class API(object):
    def __init__(self):
        pass
    
    def get_next_days(self, days: int):
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + session.params['api_key']}
        params = {'nextDays': days}
        path = 'https://api.espace.cool/api/v2/event/occurrences'
        response = session.get(path, headers=headers, params=params)
        return response.json()
