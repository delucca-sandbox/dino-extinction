import json

from random import randint
from dino_extinction.infrastructure import redis

def new_battlefield():
    battle_id = randint(999, 9999)
    initial_state = json.dumps({})

    redis.instance.set(battle_id, initial_state)

    data = dict()
    data['id'] = battle_id

    return data
