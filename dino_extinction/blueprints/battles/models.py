"""Battles Models.

This module contains all the classes and methods regarding our
battles blueprint models.

"""
import pickle

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

        Raises
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
        redis.set(battle_id, raw_data)

        return True
