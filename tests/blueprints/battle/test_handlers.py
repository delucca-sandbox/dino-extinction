"""Battle Handlers Unit Tests.

This test file will ensure that the most important logic of our Battle
blueprint's handlers are working as we are expecting.

"""
from mock import patch
from faker import Faker
from dino_extinction.blueprints.battle import handlers


@patch('dino_extinction.blueprints.battle.handlers.models')
def test_called_model(mocked_models):
    """Test the calling of our model.

    This test will ensure that our handler is calling our model during the
    creation of a new battlefield.

    ...

    Parameters
    ----------
    mocked_models : magic mock
        The mock of our battle models module.

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
    """Test the creation of a new battle ID.

    This test will ensure that we are creating a 4 digit long ID every
    time a new battle is created.

    ...

    Parameters
    ----------
    mocked_models : magic mock
        The mock of our battle models module.

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
    """Test the error handling.

    This test will ensure that we are dealing correctly with any error. More
    specifically in a case where we try to insert a wrong ID type

    ...

    Parameters
    ----------
    mocked_randint : magic mock
        The mock of the randint function, that creates our IDs.

    """
    # given
    fake = Faker()
    mocked_randint.return_value = fake.word()

    # when
    errors = handlers.new_battlefield(board_size=fake.word())[0]

    # then
    assert errors['id'] == ['Not a valid integer.']
    assert errors['board_size'] == ['Not a valid integer.']
