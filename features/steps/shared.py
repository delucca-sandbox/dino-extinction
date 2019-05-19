"""Shared Steps.

This module contains every step that is shared between multiple feature tests.
Beware to build them in a way that multiple features could use them.

"""
import json
import pickle

from faker import Faker
from behave import (given, then)
from dino_extinction.blueprints.battles.models import BattleSchema
from dino_extinction.infrastructure import redis


@given('a fake data provider')
def step_create_fake_data_provider(context):
    """Insert a fake data provider into context.

    This step will use Faker to generate a new fake data provider and
    insert it into the context in order to be used by our steps.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    fake = Faker()
    fake.provider('address')

    context.faker = fake

    assert context.faker


@given('an existing battle')
def step_create_new_battle(context):
    """Create a battle.

    This step will create a battle on our Redis using the generated
    battle_id from the current context.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    if not hasattr(context, 'board_size'):
        context.board_size = 50

    for request in context.requests:
        battle_id = request['battleId']
        if not battle_id:
            continue

        battle = dict()
        battle.setdefault('id', battle_id)
        battle.setdefault('board_size', context.board_size)

        model = BattleSchema()
        model.dumps(battle)

        assert redis.instance.get(battle_id)


@given('an non-existing battle')
def step_create_new_non_existing_batt


@then('the dinossaur was not created')
def step_check_if_the_dino_was_not_created(context):
    """Check if no dino exists.

    This step will check if we didn't have created any dino in our
    current battle.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    for request in context.requests:
        battle_id = request['battleId']
        if not battle_id:
            continue

        snapshot = pickle.loads(context.snapshots[battle_id])

        raw_battle = redis.instance.get(battle_id)
        battle = pickle.loads(raw_battle)

        assert battle == snapshotle(context):
    """Create an untracked battle.

    This step will create a battle on our Redis using an untracked battleId
    in order to create a battle that you can't interact with

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    battle = dict()
    battle.setdefault('id', 9999)
    battle.setdefault('board_size', context.board_size)

    model = BattleSchema()
    model.dumps(battle)

    assert redis.instance.get(9999)


@given('a snapshot of all battles')
def step_take_snapshots(context):
    """Take a snapshot of every battle.

    This step will take a snapshot of every battle and save it into our
    context in order to compare if afterwards.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    context.snapshots = dict()

    for request in context.requests:
        battle_id = request.get('battleId')
        snapshot = redis.instance.get(battle_id)

        context.snapshots.setdefault(battle_id, snapshot)

    assert len(context.snapshots) > 0


@then('we get a success {message}')
def step_check_requests_status(context, message):
    """Check request status.

    This step will check for all requests if all received a 200 status
    with a basic return on data.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    message : string
        The message that we want to receive from our server.

    """
    for response in context.responses:
        data = json.loads(response.data.decode('utf-8'))

        assert response.status_code == 200
        assert data == message


@then('we receive an error')
def step_check_received_an_error(context):
    """Check if we received errors.

    This step will check if our requests received errors.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    for response in context.responses:
        data = json.loads(response.data.decode('utf-8'))

        assert response.status_code == 500
        assert not data


@then('the battle state is the same')
def step_check_if_nothing_happened(context):
    """Check if nothing happens.

    This step will check that nothing has happened on our battle and it
    state is still the same.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    for request in context.requests:
        battle_id = request['battleId']
        assert battle_id

        snapshot = pickle.loads(context.snapshots[battle_id])

        raw_battle = redis.instance.get(battle_id)
        battle = pickle.loads(raw_battle)

        assert battle == snapshot
