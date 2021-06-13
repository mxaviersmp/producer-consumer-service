import json
import multiprocessing
import os

from fastapi.testclient import TestClient

from app.consumer.main import consume_queue
from app.producer.main import app


def test_produce_consume_message(mocker, tmpdir):
    """
    Tests integration between producer and consumer.

    Posts data to the '/process' endpoint.
    Checks if message was written to the file.
    """
    directory = tmpdir.mkdir('consumer')
    file_name = directory.join('output.txt')
    file_path = os.path.join(
        file_name.dirname, file_name.basename
    )

    fileobj = open(file_path, 'a', buffering=1)
    mocker.patch('app.consumer.main.FILE', fileobj)

    consumer = multiprocessing.Process(target=consume_queue)
    consumer.start()
    data = {
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
    }
    with TestClient(app) as client:
        response = client.post('/process', json=data)
        assert response.status_code == 200, 'Get not successfull'
    consumer.terminate()
    fileobj.close()

    with open(file_name, 'r') as f:
        file_contents = [line.strip() for line in f.readlines()]

    assert file_contents == [json.dumps(data)], 'Wrong file content'
