from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.producer.main import app

client = TestClient(app)


def test_get_root():
    """Test '/' endpoint get response."""
    response = client.get('/')
    assert response.status_code == 200, 'Get not successfull'
    assert response.json() == {'status': 'ok'}, 'Json response unexpected'


def test_head_root():
    """Test '/' endpoint head response."""
    response = client.head('/')
    assert response.status_code == 200, 'Get not successfull'
    assert response.headers == {
        'content-length': '4',
        'content-type': 'application/json'
    }, 'Headers unexpected'


def test_invalid_root():
    """Test '/' endpoint Not Allowed verbs."""
    response = client.options('/')
    assert response.status_code == 405, 'Code different than Not Allowed on options'
    response = client.post('/')
    assert response.status_code == 405, 'Code different than Not Allowed on post'
    response = client.put('/')
    assert response.status_code == 405, 'Code different than Not Allowed on put'
    response = client.delete('/')
    assert response.status_code == 405, 'Code different than Not Allowed on delete'


def test_post_process(mocker):
    """Test '/process' endpoint post response."""
    class AsyncMock(MagicMock):
        async def __call__(self, *args, **kwargs):
            return super(AsyncMock, self).__call__(*args, **kwargs)

    mocker.patch('app.producer.main.app.state', new_callable=AsyncMock)

    response = client.post('/process', json={
        'key_1': {
            'nested_key_2': {
                'key_3': 'im_a_string!',
                'key_4': 12,
                'nested_key_5': {
                    'key_6': 'hello',
                    'key_7': 42
                }
            }
        }
    })
    assert response.status_code == 200, 'Get not successfull'
    assert response.json() == {'result': 'Success'}, 'Json response unexpected'

    response = client.post('/process', json='1')
    assert response.status_code == 422, 'Validation failed'
    resp_json = response.json()
    assert resp_json['detail'][0]['msg'] == 'value is not a valid dict', 'Wrong msg'


def test_head_process():
    """Test '/process' endpoint head response."""
    response = client.head('/process')
    assert response.status_code == 200, 'Get not successfull'
    assert response.headers == {
        'content-length': '4',
        'content-type': 'application/json'
    }, 'Headers unexpected'


def test_invalid_process():
    """Test '/process' endpoint Not Allowed verbs."""
    response = client.options('/process')
    assert response.status_code == 405, 'Code different than Not Allowed on options'
    response = client.get('/process')
    assert response.status_code == 405, 'Code different than Not Allowed on get'
    response = client.put('/process')
    assert response.status_code == 405, 'Code different than Not Allowed on put'
    response = client.delete('/process')
    assert response.status_code == 405, 'Code different than Not Allowed on delete'
