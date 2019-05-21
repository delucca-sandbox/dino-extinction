"""Robots Handlers.

This module contains all handlers that we are going to use in our
Robots Module API. They will be used inside our routes.

"""
from copy import deepcopy
from dino_extinction.blueprints.battles.models import BattleSchema
from dino_extinction.blueprints.robots.models import RobotSchema
from . import models
from . import constants


def new_robot(battle_id, direction, board_position):
    """Create a new robot.

    This handler creates a new robot into a specific board setting it on
    the provided X and Y positions and a facing direction. It is important
    to notice that it will return an error if any of the following
    cases are true:
        * The user has not provided all parameters
        * The X and Y positions are out of range
        * There is already another entity in that position

    ...

    Parameters
    ----------
    battle_id : int
        The ID of your current battle.

    direction : string
        The direction where the robot is facing. It can be either north,
        south, east or west.

    board_position: tuple
        A tuple with a given X and Y positions to your robot.

    Returns
    -------
    errors : dict
        A dict containing every error that happened during the robot
        creation (if any).

    message : string
        A message to the user about the creation of that robot.

    """
    robot = dict()
    robot['battle_id'] = battle_id
    robot['direction'] = direction
    robot['position'] = board_position
    robot_model = models.RobotSchema()
    created_robot = robot_model.load(robot)

    return created_robot.errors, created_robot


def command_robot(battle_id, robot_id, action):
    """Command a specific robot.

    This handler will command an specific robot, at a specific battle, to do
    some given action. It must guarantee that the action is also valid and
    return any errors if it is not.

    ...

    Parameters
    ----------
    battle_id : int
        The ID of your current battle.

    robot_id : string
        The ID of the robot that will receive the action.

    action: string
        An action that can be: turn-left, turn-right, move-forward,
        move-backwards or attack.

    Returns
    -------
    errors : dict
        A dict containing every error that happened during the robot
        action (if any).

    message : string
        A message to the user about the action of that robot.

    """
    def _default_error(msg):
        return msg, None

    battle_model = BattleSchema()
    battle_state_original = battle_model.get_battle(battle_id)
    if not battle_state_original:
        return _default_error('This battle does not exist')

    entities = battle_state_original.get('entities')
    selected_robot = entities.get(robot_id)
    if not selected_robot:
        return _default_error('This robot does not exist')

    if action in constants.ACTIONS_TURNED:
        robot_model = RobotSchema()
        previous_direction = selected_robot.get('direction')
        new_robot_direction = robot_model.change_direction(previous_direction,
                                                           action)
        new_battle_state = deepcopy(battle_state_original)
        robot = new_battle_state.get('entities').get(robot_id)

        new_direction = dict()
        new_direction.setdefault('direction', new_robot_direction)
        robot.update(new_direction)
        battle_model.update_battle(battle_id, new_battle_state)

    if action in constants.ACTIONS_MOVED:
        new_battle_state = battle_model.robot_move(battle_state_original,
                                                   robot_id,
                                                   action)

        if not new_battle_state:
            return _default_error('There is another entity there')
        battle_model.update_battle(battle_id, new_battle_state)

    if action == 'attack':
        new_battle_state = battle_model.robot_attack(battle_state_original,
                                                     robot_id)

        battle_model.update_battle(battle_id, new_battle_state)

    return None, 'Robot commanded'
