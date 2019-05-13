"""Dinossaurs Steps.

This module contains every step to test the behaviour of our Dinossaurs
services.

"""
import json

from behave import (given, when, then)
from faker import Faker
from dino_extinction.blueprints.battles.models import BattleSchema
from dino_extinction.infrastructure import redis


@given('a fake data provider')
def step_create_fake_data_provider(context):
    """Insert a fake data provider into context.

    This function will use Faker to generate a new fake data provider and
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
    context.battle_id = context.faker.random_digit()
    context.board_size = 50

    request = dict()
    request['battleId'] = context.battle_id
    request['xPosition'] = context.faker.random_digit()
    request['yPosition'] = context.faker.random_digit()

    context.requests = [request]


@given('an existing battle')
def step_create_new_battle(context):
    """Create a battle.

    This function will create a battle on our Redis using the generated
    battle_id from the current context.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    battle = dict()
    battle['id'] = context.battle_id
    battle['board_size'] = context.board_size

    model = BattleSchema()
    model.dumps(battle)

    assert redis.instance.get(context.battle_id)


@when('we ask to create a new dinossaur')
def step_request_new_dinossaur(context):
    """Request new dinossaur.

    This function will run the request to create a new dinossaur. It can be
    multiple requests, so it will loop over the requests key into the context
    in order to run all requests.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    context.created_dinossaurs = len(context.requests)
    context.responses = [context.client.post('/dinossaurs/new',
                                             data=request,
                                             follow_redirects=True)
                         for request in context.requests]

    assert context.responses
    assert context.created_dinossaurs


@then('we receive the status of the creation')
def step_check_requests_status(context):
    """Check request status.

    This function will check for all requests if all received a 200 status
    with a basic return on data.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    for response in context.responses:
        data = json.loads(response.data.decode('utf-8'))

        assert response.status_code == 200
        assert data == 'Dinossaur created'


@then('the dinossaur was created')
def step_check_if_dinossaur_was_created(context):
    """Check if the dinossaur was created.

    This function compares the number of previous dinossaurs and how many
    were created.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    battle = redis.instance.get(context.battle_id)
    print(battle)

    assert False


@then('the battle was updated')
def step_check_if_battle_was_updated(context):
    """Check if the dinossaur was created.

    This function checks if the created dinossaurs are linked into the
    current battle state.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    battle = redis.instance.get(context.battle_id)
    print(battle)

    assert False
