"""Dinossaurs Handlers.

This module contains all handlers that we are going to use in our
Dinossaurs Module API. They will be used inside our routes.

"""
import json

from . import models

def new_dinossaur(battle_id, board_position):
    """Create a new dinossaur.

    This handler creates a new dinossaur into a specific board setting it on
    the provided X and Y positions. It is importante to notice that it will
    return an error if any of the following cases are true:
        * The user has not provided all parameters
        * The X and Y positions are out of range
        * There is already another entity in that position

    ...

    Parameters
    ----------
    battle_id : int
        The ID of your current battle.

    board_position: tuple
        A tuple with a given X and Y positions to your dinossaur.

    Returns
    .......
    errors : dict
        A dict containing every error that happened during the dinossaur
        creation (if any).

    message : string
        A message to the user about the creation of that dinossaur.

    """
    dinossaur = dict()
    dinossaur['position'] = board_position
    dinossaur_model = models.DinossaurSchema()
    created_dinossaur = dinossaur_model.dumps(dinossaur)

    return created_dinossaur.errors, created_dinossaur
