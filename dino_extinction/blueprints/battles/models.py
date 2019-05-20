"""Battles Models.

This module contains all the classes and methods regarding our
battles blueprint models.

"""
import pickle

from copy import deepcopy
from marshmallow import (Schema, fields, validates, post_dump, ValidationError)
from dino_extinction.infrastructure import redis


class BattleSchema(Schema):
    """BatttleSchema Class.

    This class is responsible for handling all data regarding our
    battles schema.

    ...

    Attributes
    ----------
    id : int
        The ID of the battle that you're handling.

    board_size : int
        The size of the board that you are creating.

    """
    id = fields.Integer(required=True)
    board_size = fields.Integer(required=True)

    @validates('id')
    def validate_id(self, data):
        """Validate the length of battle ID.

        This validator checks if the number of digits of our current
        battle ID is 4. If not, it will raise an error.

        ...

        Raises        print(original_position)

        ------
        ValidationError
            If the number of digits of the ID is different than 4.

        """
        digits = str(data)
        number_of_digits = len(digits)

        if number_of_digits != 4:
            raise ValidationError('The battle ID should be 4 digits long.')

    @post_dump
    def create_battle(self, data):
        """Create a new battle.

        This method will create a new battle if you try to dump a new
        data and all the attributes are valid.

        ...

        Parameters
        ----------
        data : dict
            A dict containing all the data that you are trying to insert into
            the new battle. Valid keys: board_size, size and state.

        """
        board_size = data['board_size']
        board_state = [[None] * board_size for _ in range(board_size)]


        board = dict()
        board['size'] = board_size
        board['state'] = board_state

        battle = dict()
        battle['board'] = board
        pickled_battle = pickle.dumps(battle)
        redis.instance.set(data['id'], pickled_battle)


    def get_battle(self, battle_id):
        """Get the data from an existing battle.

        This method will get the data from an existing battle, return it data
        normalized or None if the data does not exist.

        ...

        Parameters
        ----------
        battle_id : str
            The ID of the battle that you are trying to get.

        Returns
        -------
        battle : dict
            The data of the desired battle (if exists) normalized as a
            Python dict. If there is no battle, it should return None.

        """
        raw_data = redis.instance.get(battle_id)
        if not raw_data:
            return None

        data = pickle.loads(raw_data)

        return data

    def update_battle(self, battle_id, new_data):
        """Update the data of an existing battle.

        This method will use the new data to update and overwrite an existing
        battle data.

        ...

        Parameters
        ----------
        battle_id : str
            The ID of the battle that you are trying to update.

        new_data : dict
            The entire battle new data that will overwrite the previous data.

        """
        raw_data = pickle.dumps(new_data)
        redis.instance.set(battle_id, raw_data)

        return True

    def robot_move(self, battle, robot_id, action):
        """Move the robot inside the battlefield.

        This method will move the desired robot inside the battlefield
        according to an specific action. It will not move if any other entity
        has already taken that position.

        ...

        Parameters
        ----------
        battle : dict
            The battle object that you are working on.

        robot_id : str
            The ID of the robot that you are trying to move.

        action : str
            The action that you are trying to do. It can be? move-forward or
            move-backwards.

        """
        cardinal_points = dict()
        cardinal_points.setdefault('north', 0)
        cardinal_points.setdefault('south', 0)
        cardinal_points.setdefault('west', 1)
        cardinal_points.setdefault('east', 1)

        reversed_directions = dict()
        reversed_directions.setdefault('north', False)
        reversed_directions.setdefault('east', False)
        reversed_directions.setdefault('south', True)
        reversed_directions.setdefault('west', True)

        robot = battle.get('entities').get(robot_id)
        facing_direction = robot.get('direction')
        cardinal_point = cardinal_points.get(facing_direction)
        is_reversed = reversed_directions.get(facing_direction)

        original_position = robot.get('position')
        position_to_change = original_position[cardinal_point]
        updated_battle = deepcopy(battle)
        changed_position = self._calculate_position(position_to_change,
                                                    action,
                                                    is_reversed)

        new_robot_position = [pos for pos in original_position]
        new_robot_position[cardinal_point] = changed_position
        new_robot_position = tuple(new_robot_position)

        old_yPos = original_position[0]
        old_xPos = original_position[1]
        new_yPos = new_robot_position[0]
        new_xPos = new_robot_position[1]

        if battle.get('board').get('state')[new_yPos][new_xPos]:
            return False

        updated_battle.get('board').get('state')[old_yPos][old_xPos] = None
        updated_battle.get('board').get('state')[new_yPos][new_xPos] = robot_id

        new_position = dict()
        new_position.setdefault('position', new_robot_position)
        updated_battle.get('entities').get(robot_id).update(new_position)

        return updated_battle

    def robot_attack(self, battle, robot_id):
        """Attack all dinos close to an specific robot

        This method will destroy all dinos close to an specific robot. It will
        not attack any other robot close to it.

        ...

        Parameters
        ----------
        battle : dict
            The battle object that you are working on.

        robot_id : str
            The ID of the robot that you are trying to move.

        """
        robot = battle.get('entities').get(robot_id)
        robot_position = robot.get('position')
        entities = battle.get('entities')

        robot_yPos = robot_position[0]
        robot_xPos = robot_position[1]
        yPositions = [robot_yPos + 1, robot_yPos - 1]
        xPositions = [robot_xPos + 1, robot_xPos - 1]

        corners = [(x, y) for x in xPositions for y in yPositions]
        same_ver_axis = [(x, y) for x in robot_position for y in yPositions]
        same_hor_axis = [(x, y) for x in xPositions for y in robot_position]
        positions_to_attack = list(set().union(corners,
                                               same_ver_axis,
                                               same_hor_axis))

        for yPos, xPos in positions_to_attack:
            entity = battle.get('board').get('state')[yPos][xPos]

            if entity and entity[:2] == 'D-':
                del entities[entity]
                battle.get('board').get('state')[yPos][xPos] = None

        return battle

    def _calculate_position(self, pos, act, rev):
        def move_forward(x, rev):
            return x + 1 if not rev else x - 1

        def move_backwards(x, rev):
            return x - 1 if not rev else x + 1

        dispatch = dict()
        dispatch.setdefault('move-forward', move_forward)
        dispatch.setdefault('move-backwards', move_backwards)

        return dispatch.get(act)(pos, rev)
