import pickle

from marshmallow import (Schema, fields, validates, post_dump, ValidationError)
from itertools import product
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
        board = {i: x for i, x in enumerate(product(range(data['board_size']),
                                                    repeat=2))}

        state = dict()
        state['board'] = board
        pickled_state = pickle.dumps(state)
        redis.instance.set(data['id'], pickled_state)
