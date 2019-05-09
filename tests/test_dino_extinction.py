"""Dino Extinction Unit Tests.

This test file will ensure that the most important logic of our Dino
Extinction module are working as we are expecting.

"""
from mock import patch
from faker import Faker
from dino_extinction import create_app


@patch('dino_extinction.Flask')
@patch('dino_extinction.load_configs')
@patch('dino_extinction.redis')
def test_redis_connection(mocked_redis,
                          mocked_load_configs,
                          mocked_Flask):
    """Test redis connection.

    This test will ensure that we are binding to our redis when we try to
    create a new Flask app.

    ...

    Parameters
    ----------
    mocked_redis : magic mock
        The mock of our redis module.

    mocked_load_configs : magic mock
        The mock of the configuration loader in our Dino Extinction module.

    mocked_Flash: magic mock
        The mock of our Flask module.

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
    """Test the loading of custom configs.

    This test will check if we're loading custom configuration files when
    we try to create a new Flask app.

    ...

    Parameters
    ----------
    mocked_redis : magic mock
        The mock of our redis module.

    mocked_load_configs : magic mock
        The mock of the configuration loader in our Dino Extinction module.

    mocked_Flash: magic mock
        The mock of our Flask module.

    """
    # given
    fake = Faker()
    fake.add_provider('python')

    expected = fake.word()

    mocked_load_configs.return_value = {'morty': expected}

    # when
    app = create_app()

    # then
    assert app.config['morty'] == expected
