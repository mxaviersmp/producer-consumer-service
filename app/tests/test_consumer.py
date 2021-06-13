import os

from app.consumer.main import callback


def test_callback(tmpdir, mocker):
    """Test callback for queue consumer."""
    class PikaMock:
        def __init__(self):
            self.deliveries = []
            self.delivery_tag = 1

        def basic_ack(self, delivery_tag):
            self.deliveries.append(delivery_tag)

        def basic_nack(self, delivery_tag, requeue):
            self.deliveries.append((delivery_tag, requeue))

    directory = tmpdir.mkdir('consumer')

    file_name = directory.join('output.txt')

    file_path = os.path.join(
        file_name.dirname, file_name.basename
    )

    fileobj = open(file_path, 'a', buffering=1)
    mocker.patch('app.consumer.main.FILE', fileobj)

    pika_mock = PikaMock()
    callback(pika_mock, pika_mock, pika_mock, b'{"test": 1}')

    with open(file_name, 'r') as f:
        file_contents = f.readlines()

    assert pika_mock.deliveries == [1], 'Failed to ack message'
    assert file_contents == ['{"test": 1}\n'], 'Wrong file content'

    callback(pika_mock, pika_mock, pika_mock, b"{'test': 1}")

    with open(file_name, 'r') as f:
        file_contents = f.readlines()

    assert pika_mock.deliveries == [1, (1, False)], 'Failed to ack message'
    assert file_contents == ['{"test": 1}\n'], 'Wrong file content'

    fileobj.close()
