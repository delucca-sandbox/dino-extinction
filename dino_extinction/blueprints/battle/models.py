import json

from marshmallow import (Schema, fields, validates, post_dump, ValidationError)
from dino_extinction.infrastructure import redis

class BattleSchema(Schema):
    id = fields.Integer(required=True)
    state = fields.Dict(default={})

    @validates('id')
    def validate_id(self, data):
        digits = str(data)
        number_of_digits = len(digits)

        if number_of_digits != 4:
            raise ValidationError('The battle ID should be 4 digits long.')

    @post_dump
    def create_battle(self, data):
        json_state = json.dumps(data['state'])
        redis.instance.set(data['id'], json_state)
