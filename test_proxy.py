#!/usr/bin/python3
import pytest
import json
import mock
from application import application, start_server


@pytest.fixture
def client():
    application.config['TESTING'] = True
    with application.test_client() as client:
        with application.app_context():
            start_server()
            yield client


class MockedResponse:
    """ Class to be used in requests mock
    """

    def __init__(self, response, status_code):
        self.content_dict = response
        self.content = json.dumps(response)
        self.status_code = status_code

    def json(self):
        return self.content_dict


@mock.patch("requests.request")
def test_proxy(request_mock, client):
    """Mock the proxy and check the headers"""
    request_mock.return_value = MockedResponse(
        {'result': 'created successfully'}, 201)
    proxy_response = client.post(
        '/api/users', headers={'Content-Type': 'application/json'})

    assert proxy_response.status == '201 CREATED'
    # By testing the json value, we confirm the header has passed
    # through correctly
    assert proxy_response.json['result'] == 'created successfully'


def test_status(client):
    """Just test we are getting the page"""

    rv = client.get('/status')
    assert b'Uptime:' in rv.data
