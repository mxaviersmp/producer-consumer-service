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

    d = tmpdir.mkdir('consumer')

    file_write_default = d.join('output.txt')

    filename_write_default = os.path.join(
        file_write_default.dirname, file_write_default.basename
    )

    fileobj = open(filename_write_default, 'a', buffering=1)
    mocker.patch('app.consumer.main.FILE', fileobj)

    pika_mock = PikaMock()
    callback(pika_mock, pika_mock, pika_mock, b'{"test": 1}')

    with open(file_write_default, 'r') as f:
        file_contents = f.readlines()

    assert pika_mock.deliveries == [1]
    assert file_contents == ['{"test": 1}\n']

    callback(pika_mock, pika_mock, pika_mock, b"{'test': 1}")

    with open(file_write_default, 'r') as f:
        file_contents = f.readlines()

    assert pika_mock.deliveries == [1, (1, False)]
    assert file_contents == ['{"test": 1}\n']

    fileobj.close()
