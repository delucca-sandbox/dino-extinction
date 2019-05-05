import json

from random import randint
from . import models

def new_battlefield():
    battle = dict()
    battle['id'] = randint(999, 9999)

    model = models.BattleSchema()
    created_battle = model.dumps(battle)

    return created_battle.errors, battle
