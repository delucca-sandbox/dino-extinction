import pickle

from marshmallow import (Schema, fields, validates, post_dump, ValidationError)
from dino_extinction.infrastructure import redis

class BattleSchema(Schema):
    id = fields.Integer(required=True)
    board_size = fields.Integer(required=True)

    @validates('id')
    def validate_id(self, data):
        digits = str(data)
        number_of_digits = len(digits)

        if number_of_digits != 4:
            raise ValidationError('The battle ID should be 4 digits long.')

    @post_dump
    def create_battle(self, data):
        board_size = data['board_size']
        board_state = [[None] * board_size for _ in range(board_size)]

        board = dict()
        board['size'] = board_size
        board['state'] = board_state

        battle = dict()
        battle['board'] = board
        pickled_battle = pickle.dumps(battle)
        redis.instance.set(data['id'], pickled_battle)
