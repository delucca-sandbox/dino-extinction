import json

from random import randint
from . import models

def new_battlefield(board_size=50):
    battle = dict()
    battle['id'] = randint(999, 9999)
    battle['board_size'] = board_size

    model = models.BattleSchema()
    created_battle = model.dumps(battle)

    return created_battle.errors, battle
