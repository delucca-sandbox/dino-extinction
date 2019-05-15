"""Dinossaurs Models.

This module contains all the classes and methods regarding our
dinossaurs blueprint models.

"""
import pickle

from random import randint
from marshmallow import (Schema, fields, validates, post_dump, ValidationError)
from dino_extinction.infrastructure import redis
from . import constants


class DinossaurSchema(Schema):
    """DinosaurSchema Class.

    This class is responsible for handling all data regarding our
    dinossaurs schema.

    ...

    Attributes
    ----------
    battle_id : int
        The ID of the battle that you're handling.

    position : tuple
        An X and Y position tuple storing where your dinossaur is.

    """
    battle_id = fields.Integer(required=True)
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

    @post_dump
    def create_dinossaur(self, data):
        """Create a new dinossaur.

        This method will create a new dinossaur if you try to dump a new
        data and all the attributes are valid.

        ...

        Parameters
        ----------
        data : dict
            A dict containing all the data that you are trying to insert into
            the new battle. Valid keys: battle_id and position.

        """
        battle_id = data['battle_id']
        position = data['position']
        xPos = position[0] - 1
        yPos = position[1] - 1

        dinossaur_id = self._create_dino_id()

        dinossaur = dict()
        dinossaur['id'] = dinossaur_id
        dinossaur['type'] = constants.TYPE
        dinossaur['position'] = position

        raw_battle = redis.instance.get(battle_id)
        if not raw_battle:
            raise ValidationError('Invalid battleId')

        battle = pickle.loads(raw_battle)
        board = battle['board']['state']
        if self._is_not_valid_index(xPos, yPos, board):
            raise ValidationError('This position is out of range')

        if board[xPos][yPos]:
            raise ValidationError('This position is not empty')

        battle.setdefault('entities', {}).update({dinossaur_id: dinossaur})
        board[xPos][yPos] = dinossaur_id

        pickled_battle = pickle.dumps(battle)
        redis.instance.set(battle_id, pickled_battle)

        return dinossaur

    def _create_dino_id(self):
        r = randint(0000, 9999)
        return 'D-{0:04d}'.format(r)

    def _is_not_valid_index(self, x, y, board):
        return x not in range(len(board[0])) or y not in range(len(board))
