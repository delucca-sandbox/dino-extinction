"""Robots Handlers.

This module contains all handlers that we are going to use in our
Robots Module API. They will be used inside our routes.

"""
from . import models


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
