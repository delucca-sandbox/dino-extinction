"""Redis Unit Tests.

This test file will ensure that the most important logic of our Redis module
are working as we are expecting.

"""
from mock import patch
from faker import Faker
from dino_extinction.infrastructure import redis


@patch('dino_extinction.infrastructure.redis.instance')
def test_new_redis_instance(mocked_instance):
    """Test instance creation.

    This test will ensure that we're creating a new Redis instance for our
    Flask app.

    ...

    Parameters
    ----------
    mocked_instance: magic mock
        The mock of the instance in our redis.

    """
    # given
    fake = Faker()
    app = fake.word()

    # when
    redis.bind(app)

    # then
    assert mocked_instance.init_app.call_count == 1
    mocked_instance.init_app.assert_called_with(app)
