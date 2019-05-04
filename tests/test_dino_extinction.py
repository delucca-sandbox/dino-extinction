from mock import patch
from faker import Faker
from dino_extinction import create_app

@patch('dino_extinction.Flask')
@patch('dino_extinction.load_configs')
@patch('dino_extinction.redis')
def test_redis_connection(mocked_redis,
                          mocked_load_configs,
                          mocked_Flask):
    """
    This test ensures that our create_app function is assigning
    a Redis instance on startup
    """
    # when
    create_app()

    # then
    assert mocked_redis.bind.call_count == 1


@patch('dino_extinction.Flask')
@patch('dino_extinction.load_configs')
@patch('dino_extinction.redis')
def test_load_custom_configs(mocked_redis,
                             mocked_load_configs,
                             mocked_Flask):
    """
    This test ensures that our created app will
    receive our custom configs
    """
    # given
    fake = Faker()
    fake.add_provider('python')

    expected = fake.word()

    mocked_load_configs.return_value = { 'morty': expected }

    # when
    app = create_app()

    # then
    assert app.config['morty'] == expected
