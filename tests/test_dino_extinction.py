from faker import Faker
from dino_extinction import create_app


def test_assign_a_redis_instance_on_startup():
    """
    This test ensures that our create_app function is assigning
    a Redis instance on startup
    """
    # # given
    # fake = Faker()
    # fake.add_provider('python')
    # mocked_redis = mocker.patch('dino_extinction.infrastructure.redis')
    #
    # host = fake.word()
    # port = fake.pyint()
    # mocked_configs = { 'host': host, 'port': port }
    #
    # mocker.patch('flask.Flask')
    # mocker.patch('dino_extinction.load_config', return_value=mocked_configs)
    #
    # # when
    # create_app()

    # then
    assert True == False
