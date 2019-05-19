"""Robots Models.

This module contains all the classes and methods regarding our
robots blueprint models.

"""
import pickle

from random import randint
from marshmallow import (Schema, fields, validates, post_load, ValidationError)
from dino_extinction.infrastructure import redis
from . import constants


class RobotSchema(Schema):
    """RobotSchema Class.

    This class is responsible for handling all data regarding our
    robots schema.

    ...

    Attributes
    ----------
    battle_id : int
        The ID of the battle that you're handling.

    direction : string
        The direction where your robot is facing (north, south, west or east)

    position : tuple
        An X and Y position tuple storing where your dinossaur is.

    """
    battle_id = fields.Integer(required=True)
    direction = fields.String(required=True)
    position = fields.List(fields.Integer, required=True)

    @validates('battle_id')
    def validate_battle_id(self, data):
        """Validate the length of battle ID.

        This validator checks if the number of digits of our current
        battle ID is 4. If not, it will raise an error.

        ...

        Raises
        ------
        ValidationError
            If the number of digits of the ID is different than 4.

        """
        digits = str(data)
        number_of_digits = len(digits)

        if number_of_digits != 4:
            raise ValidationError('The battle ID should be 4 digits long.')

    @validates('direction')
    def validate_robot_direction(self, data):
        """Validate the the robot direction.

        This validator checks if the direction that was chosen is any of
        the following: north, south, east or west.

        ...

        Raisesordered_cardinal_points = dict()
        ordered_cardinal_points.setdefault('turn-left', ordered_to_left)
        ordered_cardinal_points.setdefault('turn-right', ordered_to_right)

        cardinal_choosen = ordered_cardinal_points.get(action)
        prev_index = cardinal_choosen.index(prev) + 1
        next_index = cardinal_choosen.index(next_index) + 1

        return next_index - prev_index == 1 or 3
        ------
        ValidationError
            If the direction is not valid.

        """
        allowed_directions = ['north', 'south', 'west', 'east']

        if data not in allowed_directions or not data:
            raise ValidationError(f"The direction must be "
                                  f"north, south, west or east")

    @validates('position')
    def validate_robot_position(self, data):
        """Validate the the robot position.

        This validator checks if the position was provided with both X and Y
        positions declared.

        ...

        Raises
        ------
        ValidationError
            If the position is not valid

        """
        if len(data) != 2:
            raise ValidationError('You must provide xPos and yPos')

    @post_load
    def create_robot(self, data):
        """Create a new robot.

        This method will create a new robot if you try to dump a new
        data and all the attributes are valid.

        ...

        Parameters
        ----------
        data : dict
            A dict containing all the data that you are trying to insert into
            the new battle. Valid keys: battle_id, direction and position.

        """
        battle_id = data['battle_id']
        direction = data['direction']
        position = data['position']
        xPos = position[0] - 1
        yPos = position[1] - 1

        robot_id = self._create_robot_id()

        robot = dict()
        robot['id'] = robot_id
        robot['type'] = constants.TYPE
        robot['direction'] = direction
        robot['position'] = position

        raw_battle = redis.instance.get(battle_id)
        if not raw_battle:
            raise ValidationError('Invalid battleId')

        battle = pickle.loads(raw_battle)
        board = battle['board']['state']
        if self._is_not_valid_index(xPos, yPos, board):
            raise ValidationError('This position is out of range')

        if board[xPos][yPos]:
            raise ValidationError('This position is not empty')

        battle.setdefault('entities', {}).update({robot_id: robot})
        board[xPos][yPos] = robot_id

        pickled_battle = pickle.dumps(battle)
        redis.instance.set(battle_id, pickled_battle)

        return robot

    def change_direction(self, previous_direction, action):
        """Change the direction of a robot.

        This method will change the direction of a robot based on an specific
        action. It will turn counterclockwise if the direction is to turn-left
        and clockwise if it is turn-right.

        ...

        Parameters
        ----------
        previous_direction : str
            The previous direction of the robot.

        action : str
            The action that the user is trying to do.


        Returns
        -------
        new_direction: str
            The new direction that is the result of the action in the specific
            previous direction.

        """
        cardinal_points = dict()
        cardinal_points.setdefault('turn-right', constants.CARDINAL_CLOCKWISE)
        cardinal_points.setdefault('turn-left',
                                   constants.CARDINAL_COUNTERCLOCKWISE)

        cardinal_choosen = cardinal_points.get(action)
        prev_index = cardinal_choosen.index(previous_direction)
        next_index = prev_index + 1 if prev_index < 3 else 0
        new_direction = cardinal_choosen[next_index]

        return new_direction


    def _create_robot_id(self):
        r = randint(0000, 9999)
        return 'R-{0:04d}'.format(r)

    def _is_not_valid_index(self, x, y, board):
        return x not in range(len(board[0])) or y not in range(len(board))
