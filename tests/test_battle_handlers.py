from mock import patch
from faker import Faker
from dino_extinction.blueprints.battle import handlers


@patch('dino_extinction.blueprints.battle.handlers.redis')
def test_new_battlefield_created_on_redis(mocked_redis):
    """
    This test ensures that our handler are able to create a new
    battlefield on our redis store
    """
    # when
    result = handlers.new_battlefield()

    # then
    assert mocked_redis.instance.set.call_count == 1
    mocked_redis.instance.set.assert_called_with(result['id'], '{}')


@patch('dino_extinction.blueprints.battle.handlers.redis')
def test_multiple_battlefields_created(mocked_redis):
    """
    This test ensures that our handle are able to create multiple
    battlefields upon request
    """
    # when
    first_battlefield = handlers.new_battlefield()
    second_battlefield = handlers.new_battlefield()

    # then
    assert mocked_redis.instance.set.call_count == 2
    assert first_battlefield['id'] != second_battlefield['id']
