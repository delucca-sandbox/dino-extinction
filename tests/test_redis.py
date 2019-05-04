from mock import patch
from faker import Faker
from dino_extinction.infrastructure import redis


@patch('redis.Redis')
def test_new_redis_instance(mock_Redis):
    """
    This test ensures that we can create a new Redis instance
    """
    # given
    fake = Faker()
    fake.add_provider('python')

    host = fake.word()
    port = fake.pyint()

    # when
    redis.instance(host=host, port=port)

    # then
    assert mock_Redis.call_count == 1
    mock_Redis.assert_called_with(host=host, port=port)
