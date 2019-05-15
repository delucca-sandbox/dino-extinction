"""Battles Steps.

This module contains every step to test the behaviour of our Battles
services.

"""
import pickle
import json

from behave import (given, when, then)
from mock import patch
from faker import Faker
from dino_extinction.infrastructure import redis

###
### GIVEN STEPS
###

@given('a valid new battle request')
def step_generate_valid_request(context):
    """Generate a valid request.

    This step will generate a valid request for a new battle.

    ...

    Parameters
    ----------
    context : behave context
        The behave context of the current feature test.

    """
    context.board_size = 50

    request = dict()

    context.requests = [request]


@given('a valid new battle request asking for 2x2 grid')
def step_generate_request_2x2(context):
    """Generate a valid request asking for a 2x2 grid.

    This step will generate a valid request payload asking for a 2x2
    battle grid.

    ...

    Parameters
    ----------
    context : behave context
        The behave context of the current feature test.

    """
    context.board_size = 2

    request = dict()
    request.setdefault('size', context.board_size)

    context.requests = [request]

###
### WHEN STEPS
###

@when('we ask to create a new battle')
def step_create_new_battle(context):
    """Create a new battle request.

    This step will do a post request to our battle service asking
    to create all the battles that are set in the requests context.

    ...

    Parameters
    ----------
    context : behave context
        The behave context of the current feature test.

    """
    context.created_battles = len(context.requests)
    context.responses = [context.client.post('/battles/new',
                                             data=request,
                                             follow_redirects=True)
                         for request in context.requests]

    assert context.responses
    assert context.created_battles


@when('we create an invalid battle')
@patch('dino_extinction.blueprints.battles.handlers.randint')
def step_handle_error(context, mocked_randint):
    """Create a new battle request mocking for an error.

    This step will do a post request to our battle service asking
    to create a new battle using the params from our context, but it
    will also mock the ID generation of the battle in order to fail.

    ...

    Parameters
    ----------
    context : behave context
        The behave context of the current feature test.

    mocked_randint : magic mock
        The mocked randint function mocker.

    """
    fake = Faker()
    battle_id = fake.word()
    mocked_randint.return_value = battle_id

    context.battle_ids = [battle_id]
    context.created_battles = len(context.requests)
    context.responses = [context.client.post('/battles/new',
                                             data=request,
                                             follow_redirects=True)
                         for request in context.requests]

    assert context.responses
    assert context.created_battles

###
### THEN STEPS
###

@then('we receive the battle ID')
def step_assert_received_battle_id(context):
    """Assert that we received the battle ID.

    This step will assert that our service is responding with the
    created battle ID.

    ...

    Parameters
    ----------
    context : behave context
        The behave context of the current feature test.

    """
    context.battle_ids = []

    for response in context.responses:
        result = json.loads(response.data.decode('utf-8'))
        context.battle_ids.append(result['id'])

        assert response.status_code == 200
        assert result['id']


@then('the battle was created')
def step_assert_battle_was_created(context):
    """Assert that the battle was created.

    This step will check on Redis if the battle was successfully
    created.

    ...

    Parameters
    ----------
    context : behave context
        The behave context of the current feature test.

    """
    for battle_id in context.battle_ids:
        assert redis.instance.get(battle_id)


@then('the battle was not created')
def step_assert_battle_not_created(context):
    """Assert battle was not created.

    This step will ensure that the battle was not created on Redis if
    anything goes wrong in our service.

    ...

    Parameters
    ----------
    context : behave context
        The behave context of the current feature test.

    """
    for battle_id in context.battle_ids:
        assert not redis.instance.get(battle_id)


@then('we stored a 2x2 battle')
def step_assert_stored_battle(context):
    """Assert stored battle with custom size.

    This step will ensure that we can create a new battle with a custom
    grid size.

    ...

    Parameters
    ----------
    context : behave context
        The behave context of the current feature test.

    """
    for battle_id in context.battle_ids:
        data = redis.instance.get(battle_id)
        battle = pickle.loads(data)
        expected_state = [[None, None], [None, None]]
        board = battle['board']

        assert board['state'] == expected_state
        assert board['size'] == 2
