"""Robots Steps.

This module contains every step to test the behaviour of our Robots
services.

"""
import pickle

from collections import Counter
from behave import (given, when, then)
from dino_extinction.blueprints.robots.models import RobotSchema
from dino_extinction.infrastructure import redis


@given('a valid new robot request')
def step_create_request(context):
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
    request.setdefault('direction', 'north')

    context.requests = [request]


@given('a set of new robot requests')
def step_create_set_of_requests(context):
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
        fields = ['battleId', 'xPosition', 'yPosition', 'direction']

        return {field: row[field] for field in fields}

    context.requests = [request_template(row) for row in context.table]
    assert context.requests


@given('a robot already at that place')
def step_insert_robot_at_desired_position(context):
    """Insert a robot at desired position.

    This step will generate a robot at every place that we are trying
    to insert dinossaurs to.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    model = RobotSchema()

    for request in context.requests:
        data = dict()
        data.setdefault('battle_id', request.get('battleId'))
        data.setdefault('direction', 'north')
        data.setdefault('position', (request.get('xPosition'),
                                     request.get('yPosition')))

        model.load(data)


@when('we ask to create a new robot')
def step_ask_to_create_robot(context):
    """Request new robot.

    This step will run the request to create a new robot. It can be
    multiple requests, so it will loop over the requests key into the context
    in order to run all requests.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    context.created_robots = len(context.requests)
    context.responses = [context.client.post('/robots/new',
                                             data=request,
                                             follow_redirects=True)
                         for request in context.requests]

    assert context.responses
    assert context.created_robots


@then('the robot was created')
def step_check_if_robot_was_created(context):
    """Check if the robot was created.

    This step compares the number of previous robots and how many
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

        robots_created = Counter(k['battleId'] for k in context.requests)
        current_request_robots = robots_created.get(battle_id)

        assert 'entities' in battle
        assert len(entities) == current_request_robots

        xPos = int(request['xPosition'])
        yPos = int(request['yPosition'])
        robot_id = board[xPos - 1][yPos - 1]

        assert robot_id in entities
        assert entities[robot_id]['position'] == [xPos, yPos]
        assert entities[robot_id]['direction'] == request['direction']


@then('the robot was not created')
def step_check_if_robot_was_not_created(context):
    """Check if no robot exists.

    This step will check if we didn't have created any robot in our
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
