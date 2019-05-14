"""Dinossaurs Steps.

This module contains every step to test the behaviour of our Dinossaurs
services.

"""
import json
import pickle

from behave import (given, when, then)
from faker import Faker
from dino_extinction.blueprints.battles.models import BattleSchema
from dino_extinction.blueprints.dinossaurs.models import DinossaurSchema
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


@given('a valid new dinossaur request')
def step_generate_valid_request(context):
    """Generate a valid request.

    This step will generate a valid request with fake data for the
    current context.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    context.board_size = 50

    request = dict()
    request.setdefault('battleId', context.faker.random_digit())
    request.setdefault('xPosition', context.faker.random_digit())
    request.setdefault('yPosition', context.faker.random_digit())

    context.requests = [request]


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
def step_create_new_non_existing_battle(context):
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


@given('a set of new dinossaur requests')
def step_set_of_requests(context):
    """Generate a set of requests.

    This step will generate a set of requests based on some data that was
    provided in the feature file.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    context.battle_id = 1
    context.board_size = 50

    def request_template(row):
        r = dict()
        r.setdefault('battleId', row['battleId'])
        r.setdefault('xPosition', row['xPosition'])
        r.setdefault('yPosition', row['yPosition'])

        return r

    context.requests = [request_template(row) for row in context.table]
    assert context.requests


@given('and a dinossaur already at that place')
def step_insert_an_inconvenient_dinossaur(context):
    """Insert an inconvenient dinossaur.

    This step will generate a dinossaur at every place that we are trying
    to insert dinossaurs to.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    model = DinossaurSchema()

    for request in context.requests:
        data = dict()
        data.setdefault('battle_id', request.get('battleId'))
        data.setdefault('position', (request.get('xPosition'),
                                     request.get('yPosition')))

        model.dumps(data)


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


@when('we ask to create a new dinossaur')
def step_request_new_dinossaur(context):
    """Request new dinossaur.

    This step will run the request to create a new dinossaur. It can be
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

    This step will check for all requests if all received a 200 status
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

    This step compares the number of previous dinossaurs and how many
    were created.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    for request in context.requests:
        battle_id = request['battleId']
        raw_battle = redis.instance.get(battle_id)
        battle = pickle.loads(raw_battle)
        board = battle['board']['state']
        entities = battle['entities']

        assert 'entities' in battle
        assert len(entities) == len(context.requests)

        xPos = request['xPosition']
        yPos = request['yPosition']
        dino_id = board[xPos][yPos]

        assert dino_id in entities
        assert entities[dino_id]['position'] == [xPos, yPos]


@then('we receive an dino error')
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


@then('the dinossaur was not created')
def step_check_if_the_dino_doesnt_exist(context):
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

        assert battle == snapshot
