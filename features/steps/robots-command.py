"""Robots Steps.

This module contains every step to test the behaviour of our Command endpoint
of our Robots service.

"""
import random
import math
import pickle

from behave import (given, when, then)
from mock import patch
from operator import add, sub
from dino_extinction.blueprints.robots.models import RobotSchema
from dino_extinction.blueprints.dinossaurs.models import DinossaurSchema
from dino_extinction.blueprints.battles.models import BattleSchema
from dino_extinction.infrastructure import redis


@given('a {command} command to a robot')
def step_create_command_request(context, command):
    """Generate a request with an specific command.

    This step will generate a valid request with fake data and with an
    specific command to a robot.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    command : string
        The command that we want to send to our robot.

    """
    battle_id = context.faker.random_int(min=1111, max=9999)
    robot_id = f"R-{context.faker.random_int(min=1111, max=9999)}"

    request = dict()
    request.setdefault('battleId', battle_id)
    request.setdefault('robot', robot_id)
    request.setdefault('action', command)

    context.requests = [request]


@given('an existing robot')
@patch('dino_extinction.blueprints.robots.models.randint')
def step_create_new_robot(context, mocked_randint):
    """Create a new robot for each request on context.

    This step will create a new robot in each battle for every request that
    was set on our context.requests object.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    mocked_randint : magic mock
        The mocked randint function mocker.

    """
    for request in context.requests:
        battle_id = request['battleId']
        robot_id = request['robot']
        allowed_directions = ['north', 'south', 'east', 'west']
        middle_of_board = math.ceil(context.board_size / 2)
        mocked_randint.return_value = int(robot_id.split('-')[1])

        robot = dict()
        robot.setdefault('battle_id', battle_id)
        robot.setdefault('direction', random.choice(allowed_directions))
        robot.setdefault('position', (middle_of_board, middle_of_board))

        model = RobotSchema()
        model.load(robot)

        raw_battle = redis.instance.get(battle_id)
        battle = pickle.loads(raw_battle)

        assert battle['entities'].get(robot_id)


@given('an attack command to a robot')
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

    battle_id = context.faker.random_int(min=1111, max=9999)
    robot_id = f"R-{context.faker.random_int(min=1111, max=9999)}"

    request = dict()
    request.setdefault('battleId', battle_id)
    request.setdefault('robot', robot_id)
    request.setdefault('action', 'attack')

    context.requests = [request]


@given('an existing dinossaur close to the robot')
def step_close_dinossaur(context):
    """Add a dinossaur close to the robot.

    This step will add a dinossaur to the battle close to the robot on the
    current request.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    battle_model = BattleSchema()
    dino_model = DinossaurSchema()
    ops = (add, sub)

    for request in context.requests:
        battle_id = request.get('battleId')
        robot_id = request.get('robot')
        battle = battle_model.get_battle(battle_id)
        robot_position = battle.get('entities').get(robot_id).get('position')

        position = [random.choice(ops)(robot_position[i], 1) for i in range(2)]
        dino = dict()
        dino.setdefault('battle_id', battle_id)
        dino.setdefault('position', tuple(position))

        dino_model.load(dino)
        board_with_dino = battle_model.get_battle(battle_id).get('board')
        assert board_with_dino.get('state')[position[0] - 1][position[1] - 1]


@given('a set of new robot commands')
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
        fields = ['battleId', 'robot', 'action']

        return {field: row[field] for field in fields}

    context.requests = [request_template(row) for row in context.table]
    assert context.requests


@given('two entities, in front and backwards of the robot')
def step_block_robot_move(context):
    """Block the robot move.

    This step will add two dinossaurs. One in front of the robot and other one
    in its backwards.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    battle_model = BattleSchema()
    dino_model = DinossaurSchema()
    ops = (add, sub)

    for request in context.requests:
        battle_id = request.get('battleId')
        robot_id = request.get('robot')
        battle = battle_model.get_battle(battle_id)
        robot_data = battle.get('entities').get(robot_id)
        robot_position = robot_data.get('position')
        robot_direction = robot_data.get('direction')

        to_reverse = dict()
        to_reverse.setdefault('north', False)
        to_reverse.setdefault('south', False)
        to_reverse.setdefault('east', True)
        to_reverse.setdefault('west', True)
        is_reversed = to_reverse.get(robot_direction)

        def _calculate_position(pos, i, reversed):
            return (ops[i](pos[i], 1), pos[i]) if not reversed else (pos[i], ops[i](pos[i], 1))

        pos = [_calculate_position(robot_position, i, is_reversed) for i in range(2)]

        dino_one = dict()
        dino_one.setdefault('battle_id', battle_id)
        dino_one.setdefault('position', pos[0])
        dino_two = dict()
        dino_two.setdefault('battle_id', battle_id)
        dino_two.setdefault('position', pos[1])

        dino_model.load(dino_one)
        dino_model.load(dino_two)

        board_with_dino = battle_model.get_battle(battle_id).get('board')
        assert board_with_dino.get('state')[pos[0][0] - 1][pos[0][1] - 1]
        assert board_with_dino.get('state')[pos[1][0] - 1][pos[1][1] - 1]


@given('an existing 1x1 battle')
def step_create_new_1x1_battle(context):
    """Create a 1x1 battle.

    This step will create a battle with 1x1 size on our Redis using the
    generated battle_id from the current context.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    context.board_size = 1

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


@when('we command the robot')
def step_command_robot(context):
    """Command a robot.

    This step will run the request to command the robot. It can be
    multiple requests, so it will loop over the requests key into the context
    in order to run all requests.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    context.total_commands = len(context.requests)
    context.responses = [context.client.post('/robots/command',
                                             data=request,
                                             follow_redirects=True)
                         for request in context.requests]

    assert context.responses
    assert context.total_commands


@then('the robot moved')
def step_check_if_robot_moved(context):
    """Check if robot moved.

    This step will check if every robot from the desired requests has moved
    according to the desired actions.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    def _calculate_distance(start, end, reversed=False):
        return start - end if reversed else end - start

    def _check_if_moved(prev, next, action):
        direction = prev.get('direction')

        cardinal_orders = dict()
        cardinal_orders.setdefault('north', 0)
        cardinal_orders.setdefault('south', 0)
        cardinal_orders.setdefault('west', 1)
        cardinal_orders.setdefault('east', 1)

        prev_cardinal_order = cardinal_orders.get(direction)
        prev_position = prev.get('position')[prev_cardinal_order]

        next_cardinal_order = cardinal_orders.get(direction)
        next_position = next.get('position')[next_cardinal_order]

        is_reversed = dict()
        is_reversed.setdefault('north', False)
        is_reversed.setdefault('east', False)
        is_reversed.setdefault('south', True)
        is_reversed.setdefault('west', True)

        traveled_forward = _calculate_distance(prev_position,
                                               next_position,
                                               reversed=is_reversed.get(
                                                            direction))

        traveled_backwards = _calculate_distance(next_position,
                                                 prev_position,
                                                 reversed=is_reversed.get(
                                                            direction))

        results = dict()
        results.setdefault('move-forward', traveled_forward)
        results.setdefault('move-backwards', traveled_backwards)

        return results.get(action) == 1

    def _check_if_turned(prev, next, action):
        ordered_to_left = ['north', 'west', 'south', 'east']
        ordered_to_right = ['north', 'east', 'south', 'west']

        ordered_cardinal_points = dict()
        ordered_cardinal_points.setdefault('turn-left', ordered_to_left)
        ordered_cardinal_points.setdefault('turn-right', ordered_to_right)

        cardinal_choosen = ordered_cardinal_points.get(action)
        prev_index = cardinal_choosen.index(prev) + 1
        next_index = cardinal_choosen.index(next) + 1

        return next_index - prev_index == 1 or 3

    def _check_if_worked(prev, next, action):
        actions_turned = ['turn-left', 'turn-right']
        actions_moved = ['move-forward', 'move-backwards']

        if action in actions_turned:
            prev_state = prev.get('direction')
            next_state = next.get('direction')

            return _check_if_turned(prev_state, next_state, action)

        if action in actions_moved:
            prev_state = dict()
            prev_state.setdefault('position', prev.get('position'))
            prev_state.setdefault('direction', prev.get('direction'))

            next_state = dict()
            next_state.setdefault('position', next.get('position'))
            next_state.setdefault('direction', next.get('direction'))

            return _check_if_moved(prev_state, next_state, action)

    for request in context.requests:
        battle_id = request['battleId']
        robot_id = request['robot']

        raw_previous_battle_state = context.snapshots.get(battle_id)
        previous_battle_state = pickle.loads(raw_previous_battle_state)
        previous_state = previous_battle_state['entities'].get(robot_id)

        raw_current_battle_state = redis.instance.get(battle_id)
        current_battle_state = pickle.loads(raw_current_battle_state)
        current_state = current_battle_state['entities'].get(robot_id)

        action = request.get('action')

        assert _check_if_worked(previous_state, current_state, action)


@then('the dinossaur was destroyed')
def step_check_dino_was_destroyed(context):
    """Check if all dinos were destroyed.

    This step will check if every dino has been destroyed after an attack
    from our robots.

    ...

    Parameters
    ----------
    context : behave context
        The behave context that is being used in this feature test.

    """
    battle_model = BattleSchema()

    for request in context.requests:
        battle_id = request.get('battleId')
        battle = battle_model.get_battle(battle_id)
        entities = battle.get('entities').keys()
        existing_dinos = [dino for dino in entities if dino[:2] == 'D-']

        assert not existing_dinos
