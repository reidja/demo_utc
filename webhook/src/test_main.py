from .main import app

from fastapi.testclient import TestClient


client = TestClient(app)


def test_america_toronto_timezone():
    '''
    Ensure the webhook can handle the America/Toronto timezone.
    '''
    response = client.post(
        '/v1/timezone/webhook',
        headers={'application/type': 'json'},
        json={'timezone': 'America/Toronto'})

    result = response.json()
    assert 'local' in result
    assert 'utc' in result
    assert result['offset'] == '+4'
    assert result['timezone'] == 'America/Toronto'
