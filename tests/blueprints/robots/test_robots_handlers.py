"""Robots Handlers Unit Tests.

This test file will ensure that the most important logic of our Robots
blueprint handlers are working as we are expecting.

"""
from mock import (patch, MagicMock)
from faker import Faker
from dino_extinction.blueprints.robots import handlers


@patch('dino_extinction.blueprints.robots.handlers.models')
def test_called_model(mocked_models):
    """Call of our model.

    This test will ensure that our handler is calling our model during the
    creation of a new robot.

    ...

    Parameters
    ----------
    mocked_models : magic mock
        The mock of our dinossaur models module.

    """
    # given
    fake = Faker()
    battle_id = fake.word()
    direction = fake.word()
    board_position = fake.word()
    mocked_instance = mocked_models.RobotSchema.return_value

    # when
    handlers.new_robot(battle_id, direction, board_position)

    # then
    expected_load = dict()
    expected_load.update({'battle_id': battle_id})
    expected_load.update({'direction': direction})
    expected_load.update({'position': board_position})

    assert mocked_models.RobotSchema.call_count == 1
    mocked_instance.load.assert_called_once_with(expected_load)


@patch('dino_extinction.blueprints.robots.handlers.BattleSchema')
def test_get_battle_state(mocked_battle_schema):
    """Get the battle state.

    This test will ensure that our command handler is asking for our battle
    model to return an specific battle state.

    ...

    Parameters
    ----------
    mocked_battle_schema : magic mock
        The mock of the models from our battles service.

    """
    # given
    fake = Faker()
    battle_id = fake.word()
    mocked_battle_models = MagicMock()
    mocked_battle_schema.return_value = mocked_battle_models

    # when
    handlers.command_robot(battle_id, fake.word(), fake.word())

    # then
    mocked_battle_models.get_battle.assert_called_once_with(battle_id)


@patch('dino_extinction.blueprints.robots.handlers.BattleSchema')
def test_battle_does_not_exist(mocked_battle_schema):
    """Get an non-existant battle state.

    This test will ensure that if the battle does not exist our command
    handler will threat is properly.

    ...

    Parameters
    ----------
    mocked_battle_models : magic mock
        The mock of the models from our battles service.

    """
    # given
    fake = Faker()
    mocked_battle_models = MagicMock()
    mocked_battle_models.get_battle.return_value = None
    mocked_battle_schema.return_value = mocked_battle_models

    # when
    errors, _ = handlers.command_robot(fake.word(), fake.word(), fake.word())

    # then
    mocked_battle_models.get_battle.assert_called_once()
    assert errors


@patch('dino_extinction.blueprints.robots.handlers.BattleSchema')
def test_robot_does_not_exists(mocked_battle_schema):
    """Get an non-existant robot.

    This test will ensure that if the robot does not exists it will return
    an error.

    ...

    Parameters
    ----------
    mocked_battle_models : magic mock
        The mock of the models from our battles service.

    """
    # given
    fake = Faker()
    battle = dict()
    battle.setdefault('entities', dict())

    mocked_battle_models = MagicMock()
    mocked_battle_models.get_battle.return_value = battle
    mocked_battle_schema.return_value = mocked_battle_models

    # when
    errors, _ = handlers.command_robot(fake.word(), fake.word(), fake.word())

    # then
    mocked_battle_models.get_battle.assert_called_once()
    assert errors


# For turn actions, it should update the battle state and return

# For move actions, it should check if the action is valid and move if so

# If the move action is invalid (anything else is there), it should return an error

# For attack actions, it should remove all dinossaurs close to it

# In attack actions, it should not remove any robot (maybe this should be a feature test too)

# Should update the battle state in the end
