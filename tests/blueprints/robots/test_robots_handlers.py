"""Robots Handlers Unit Tests.

This test file will ensure that the most important logic of our Robots
blueprint handlers are working as we are expecting.

"""
import random

from copy import deepcopy
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

import random
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


@patch('dino_extinction.blueprints.robots.handlers.RobotSchema')
@patch('dino_extinction.blueprints.robots.handlers.BattleSchema')
def test_robot_update_direction(mocked_battle_schema, mocked_robot_schema):
    """Updated the direction of an existing robot.

    This test will ensure that if we ask to update the direction of an existing
    robot it will do so and not return any errors.

    ...

    Parameters
    ----------
    mocked_battle_models : magic mock
        The mock of the models from our battles service.

    mocked_robot_schema : magic mock
        The mock of the models from our robots service.

    """
    # given
    fake = Faker()
    battle_id = fake.word()
    robot_id = fake.word()
    new_direction = fake.word()
    options = ['turn-left', 'turn-right']
    action = random.choice(options)

    robot = dict()
    robot.setdefault('direction', 'north')

    entities = dict()
    entities.setdefault(robot_id, robot)

    battle = dict()
    battle.setdefault('entities', entities)

    mocked_battle_models = MagicMock()
    mocked_battle_models.get_battle.return_value = battle
    mocked_battle_schema.return_value = mocked_battle_models

    mocked_robot_models = MagicMock()
    mocked_robot_models.change_direction.return_value = new_direction
    mocked_robot_schema.return_value = mocked_robot_models

    # when
    errors, result = handlers.command_robot(battle_id, robot_id, action)

    # then
    expected_robot = dict()
    expected_robot.setdefault('direction', new_direction)

    expected_entities = dict()
    expected_entities.setdefault(robot_id, expected_robot)

    expected_battle = dict()
    expected_battle.setdefault('entities', expected_entities)

    mocked_robot_models.change_direction.assert_called_once_with(
        robot.get('direction'),
        action)
    mocked_battle_models.update_battle.assert_called_once_with(battle_id,
                                                               expected_battle)
    assert not errors
    assert result


@patch('dino_extinction.blueprints.robots.handlers.BattleSchema')
def test_robot_move(mocked_battle_schema):
    """Move the robot to a new spot.

    This test will ensure that if we ask to move the robot it will do so. It
    should pass if the robot can go forwards and backwards.

    ...

    Parameters
    ----------
    mocked_battle_models : magic mock
        The mock of the models from our battles service.

    """
    # given
    fake = Faker()
    battle_id = fake.word()
    robot_id = fake.word()
    moved_battle = fake.word()
    options = ['move-forward', 'move-backwards']
    action = random.choice(options)

    entities = dict()
    entities.setdefault(robot_id, fake.word())

    original_battle = dict()
    original_battle.setdefault('entities', entities)

    mocked_battle_models = MagicMock()
    mocked_battle_models.get_battle.return_value = original_battle
    mocked_battle_models.robot_move.return_value = moved_battle
    mocked_battle_schema.return_value = mocked_battle_models

    # when
    errors, result = handlers.command_robot(battle_id, robot_id, action)

    # then
    mocked_battle_models.robot_move.assert_called_once_with(original_battle,
                                                            robot_id,
                                                            action)
    mocked_battle_models.update_battle.assert_called_once_with(battle_id,
                                                               moved_battle)
    assert not errors
    assert result


# For attack actions, it should remove all dinossaurs close to it
@patch('dino_extinction.blueprints.robots.handlers.BattleSchema')
def test_robot_attack(mocked_battle_schema):
    """Attack with a robot.

    This test will ensure that our handle can trigger the attack with an
    specific robot when it is asked to do so.

    ...

    Parameters
    ----------
    mocked_battle_models : magic mock
        The mock of the models from our battles service.

    """
    # given
    fake = Faker()
    battle_id = fake.word()
    robot_id = fake.word()
    attacked_battle = fake.word()
    action = 'attack'

    entities = dict()
    entities.setdefault(robot_id, fake.word())

    original_battle = dict()
    original_battle.setdefault('entities', entities)

    mocked_battle_models = MagicMock()
    mocked_battle_models.get_battle.return_value = original_battle
    mocked_battle_models.robot_attack.return_value = attacked_battle
    mocked_battle_schema.return_value = mocked_battle_models

    # when
    errors, result = handlers.command_robot(battle_id, robot_id, action)

    # then
    mocked_battle_models.robot_attack.assert_called_once_with(original_battle,
                                                              robot_id)
    mocked_battle_models.update_battle.assert_called_once_with(battle_id,
                                                               attacked_battle)
    assert not errors
    assert result
