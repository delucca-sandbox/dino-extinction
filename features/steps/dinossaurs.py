"""Dinossaurs Steps.

This module contains every step to test the behaviour of our Dinossaurs
services.

"""
from behave import (given, when, then)
from faker import Faker
from dino_extinction.blueprints.battles.models import BattleSchema

@given('a valid new dinossaur request')
def step_generate_valid_request(context):
    """Generate a valid request.

    This function will generate a valid request with fake data for the
    current context.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    fake = Faker()
    fake.provider('address')

    context.battleId = fake.random_digit()

    context.params = dict()
    context.params['battleId'] = context.battleId
    context.params['xPosition'] = fake.random_digit()
    context.params['yPosition'] = fake.random_digit()


@given('an existing battle')
def step_create_new_battle(context):
    """Create a battle.

    This function will create a battle on our Redis using the generated
    battleId from the current context.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    model = models.BattleSchema()
    created_battle = model.dumps(battle)
    print(created_battle)

    assert False
