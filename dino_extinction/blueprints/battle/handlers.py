"""Battle Handlers.

This module contains all handlers that we are going to use in our
Battle Module API. They will be used inside our routes.

"""
import json

from random import randint
from . import models

def new_battlefield(board_size=50):
    """Create a new battlefield.

    This handler creates a new battlefield based on some user configurations.
    A battlefield is basically a dict containing some basic info about a new
    battle.

    Every battlefield is a square grid and they will always be empty when the
    battlefield is created. We use a grid basically as a 2 dimensional list,
    where the 1D position and 2D position of the item is basically the x and
    y of that grid in a graph.

    ...

    Parameters
    ----------
    board_size : int
        The size of the board that will be created.

    Returns
    .......
    errors : dict
        A dict containing every error that happened during the battlefield
        creation (if any).

    battlefield : dict
        A dict containing every data that we created about the battlefield.

    """
    battle = dict()
    battle['id'] = randint(999, 9999)
    battle['board_size'] = board_size

    model = models.BattleSchema()
    created_battle = model.dumps(battle)

    return created_battle.errors, battle
