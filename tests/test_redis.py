from mock import patch
from faker import Faker
from dino_extinction.infrastructure import redis

@patch('dino_extinction.infrastructure.redis.instance')
def test_new_redis_instance(mock_instance):
    """
    This test ensures that we can create a new Redis instance
    """
    # given
    fake = Faker()
    app = fake.word()

    # when
    redis.bind(app)

    # then
    assert mock_instance.init_app.call_count == 1
    mock_instance.init_app.assert_called_with(app)
