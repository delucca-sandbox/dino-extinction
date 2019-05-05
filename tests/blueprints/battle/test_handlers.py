from mock import patch
from faker import Faker
from dino_extinction.blueprints.battle import handlers


@patch('dino_extinction.blueprints.battle.handlers.models')
def test_called_model(mocked_models):
    """
    This test ensures that our handler is calling our model with
    the right arguments
    """
    # given
    mocked_instance = mocked_models.BattleSchema.return_value

    # when
    handlers.new_battlefield()

    # then
    assert mocked_models.BattleSchema.call_count == 1
    assert mocked_instance.dumps.call_count == 1


@patch('dino_extinction.blueprints.battle.handlers.models')
def test_creating_pin_id_to_battle(mocked_models):
    """
    This test ensures that our handler is calling our model
    with a 4-digit pin code for each new battle
    """
    # given
    mocked_instance = mocked_models.BattleSchema.return_value

    # when
    handlers.new_battlefield()

    # then
    calls = mocked_instance.dumps.call_args_list[0]
    args = calls[0][0]
    digits = str(args['id'])

    assert type(args['id']) is int
    assert len(digits) == 4


@patch('dino_extinction.blueprints.battle.handlers.randint')
def test_handling_model_error(mocked_randint):
    """
    This test ensures that our handler is responding an error
    if the model couldn't create a new battle
    """
    # given
    fake = Faker()
    mocked_randint.return_value = fake.word()

    # when
    result = handlers.new_battlefield()

    # then
    assert not result
