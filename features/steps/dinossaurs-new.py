"""Dinossaurs Steps.

This module contains every step to test the behaviour of our Dinossaurs
services.

"""
import pickle

from behave import (given, when, then)
from collections import Counter
from dino_extinction.blueprints.dinossaurs.models import DinossaurSchema
from dino_extinction.infrastructure import redis


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
    request.setdefault('battleId', context.faker.random_int(min=1111,
                                                            max=9999))
    request.setdefault('xPosition', context.faker.random_int(min=1, max=9))
    request.setdefault('yPosition', context.faker.random_int(min=1, max=9))

    context.requests = [request]


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
        fields = ['battleId', 'xPosition', 'yPosition']

        return {field: row[field] for field in fields}

    context.requests = [request_template(row) for row in context.table]
    assert context.requests


@given('a dinossaur already at that place')
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

        model.load(data)


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

        dinos_created = Counter(k['battleId'] for k in context.requests)
        current_request_dinos = dinos_created.get(battle_id)

        assert 'entities' in battle
        assert len(entities) == current_request_dinos

        xPos = int(request['xPosition'])
        yPos = int(request['yPosition'])
        dino_id = board[xPos - 1][yPos - 1]

        assert dino_id in entities
        assert entities[dino_id]['position'] == [xPos, yPos]


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

        assert battle == snapshot
