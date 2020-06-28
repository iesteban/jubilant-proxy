import pytest

from application import application, start_server


@pytest.fixture
def client():
    application.config['TESTING'] = True
    with application.test_client() as client:
        with application.app_context():
            start_server()
            yield client


def test_status(client):
    """Just test we are getting the page"""

    rv = client.get('/status')
    assert b'Uptime:' in rv.data
