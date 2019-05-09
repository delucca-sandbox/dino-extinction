"""Battlefield Steps.

This module contains every step to test the behaviour of our battlefield
services.

"""
import pickle
import json

from behave import (given, when, then)
from mock import patch
from faker import Faker
from dino_extinction.infrastructure import redis


@given('a valid request')
def step_generate_valid_request(context):
    """Generate a valid request.

    This function will generate a valid request for a new battlefield.

    ...

    Parameters
    ----------
    context : behave context
        The behave context of the current feature test.

    """
    context.params = {}


@given('a valid request asking for 2x2 grid')
def step_generate_request_2x2(context):
    """Generate a valid request asking for a 2x2 grid.

    This function will generate a valid request payload asking for a 2x2
    battlefield grid.

    ...

    Parameters
    ----------
    context : behave context
        The behave context of the current feature test.

    """
    context.params = {'size': 2}


@when('we create a new battlefield')
def step_create_new_battlefield(context):
    """Create a new battlefield request.

    This function will do a post request to our battlefield service asking
    to create a new battlefield using the params from our context.

    ...

    Parameters
    ----------
    context : behave context
        The behave context of the current feature test.

    """
    context.response = context.client.post('/battle/new',
                                           data=context.params,
                                           follow_redirects=True)

    assert context.response


@when('we create an invalid battlefield')
@patch('dino_extinction.blueprints.battle.handlers.randint')
def step_handle_error(context, mocked_randint):
    """Create a new battlefield request mocking for an error.

    This function will do a post request to our battlefield service asking
    to create a new battlefield using the params from our context, but it
    will also mock the ID generation of the battlefield in order to fail.

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

    context.response = context.client.post('/battle/new',
                                           data=context.params,
                                           follow_redirects=True)

    assert context.response

    context.battle_id = battle_id


@then('we receive the battlefield ID')
def step_assert_received_battlefield_id(context):
    """Assert that we received the battlefield ID.

    This function will assert that our service is responding with the
    created battlefield ID.

    ...

    Parameters
    ----------
    context : behave context
        The behave context of the current feature test.

    """
    assert context.failed is False
    assert context.response.status_code == 200

    response = json.loads(context.response.data.decode('utf-8'))
    assert response['id']

    context.battle_id = response['id']


@then('the battlefield was created')
def step_assert_battlefield_was_created(context):
    """Assert that the battlefield was created.

    This function will check on Redis if the battlefield was successfully
    created.

    ...

    Parameters
    ----------
    context : behave context
        The behave context of the current feature test.

    """
    assert redis.instance.get(context.battle_id)


@then('we receive an error')
def step_assert_error_received(context):
    """Assert that we received an error.

    This function will check if we have received an error if anything goes
    wrong in our server.

    ...

    Parameters
    ----------
    context : behave context
        The behave context of the current feature test.

    """
    assert context.failed is False
    assert context.response.status_code == 500

    json.loads(context.response.data.decode('utf-8'))


@then('the battlefield was not created')
def step_assert_battlefield_not_created(context):
    """Assert battlefield was not created.

    This test will ensure that the battlefield was not created on Redis if
    anything goes wrong in our service.

    ...

    Parameters
    ----------
    context : behave context
        The behave context of the current feature test.

    """
    assert not redis.instance.get(context.battle_id)


@then('we stored a 2x2 battlefield')
def step_assert_stored_battlefield(context):
    """Assert stored battlefield with custom size.

    This test will ensure that we can create a new battlefield with a custom
    grid size.

    ...

    Parameters
    ----------
    context : behave context
        The behave context of the current feature test.

    """
    data = redis.instance.get(context.battle_id)
    battle = pickle.loads(data)
    expected_state = [[None, None], [None, None]]
    board = battle['board']

    assert board['state'] == expected_state
    assert board['size'] == 2
