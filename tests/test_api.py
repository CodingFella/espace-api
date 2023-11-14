# tests/test_api.py

from pytest import fixture
from espacewrapper import API
import vcr

@fixture
def status_code():
    return ['IsSuccessStatusCode']

@vcr.use_cassette('tests/vcr_cassettes/events.yml', filter_query_parameters=['api_key'])
def test_status(status_code):
    """Tests if API is working"""
    
    api_instance = API()
    response = api_instance.get_next_days(1)
    
    assert response['IsSuccessStatusCode'] == True