"""Robots Models Unit Tests.

This test file will ensure that the most important logic of our Robots
blueprint models are working as we are expecting.

"""
import pickle
import random

from faker import Faker
from mock import patch
from dino_extinction.blueprints.robots import models


@patch('dino_extinction.blueprints.robots.models.redis')
def test_generate_robot_model(mocked_redis):
    """Create a new robot.

    This test will try to create a new robot based on our model and ensure
    that it is working properly.

    ...

    Parameters
    ----------
    mocked_redis : magic mock
        The mock of our Redis module.

    """
    # given
    fake = Faker()
    fake.provider('address')
    allowed_directions = ['north', 'south', 'west', 'east']
    id = fake.random_int(min=1111, max=9999)
    direction = allowed_directions[fake.random_int(min=0, max=3)]
    position = [fake.random_int(min=1, max=9), fake.random_int(min=1, max=9)]

    state = [[None] * 9 for _ in range(9)]

    board = dict()
    board.setdefault('state', state)

    battle = dict()
    battle.setdefault('board', board)

    pickled_battle = pickle.dumps(battle)
    mocked_redis.instance.get.return_value = pickled_battle

    robot = dict()
    robot['battle_id'] = id
    robot['direction'] = direction
    robot['position'] = position

    # when
    model = models.RobotSchema()
    model.load(robot)

    # then
    called_id, raw_args = mocked_redis.instance.set.call_args_list[0][0]
    args = pickle.loads(raw_args)
    robot_id = next(iter(args['entities']))
    created_robot = args['entities'][robot_id]

    assert called_id == id
    assert len(args['entities']) == 1
    assert created_robot['type'] == 'ROBOT'
    assert created_robot['direction'] == direction
    assert created_robot['position'] == position
    mocked_redis.instance.get.assert_called_once_with(id)


def test_id_must_be_int():
    """Validate ID type.

    This test will try to insert an invalid ID data and check if our model
    is refusing any inputs that are not integers.

    """
    # given
    fake = Faker()
    fake.provider('python')
    allowed_directions = ['north', 'south', 'west', 'east']
    robot = dict()
    robot['battle_id'] = fake.word()
    robot['direction'] = allowed_directions[fake.random_int(min=0, max=3)]
    robot['position'] = [fake.random_int(min=1, max=9), fake.random_int(min=1, max=9)]

    # when
    model = models.RobotSchema()
    result = model.load(robot)

    # then
    assert 'battle_id' not in result.data
    assert result.errors['battle_id'][0] == 'Not a valid integer.'


def test_position_must_be_a_list():
    """Validate position type.

    This test will try to insert an invalid position data and check if our
    model is refusing any inputs that are not lists.

    """
    # given
    fake = Faker()
    fake.provider('python')
    allowed_directions = ['north', 'south', 'west', 'east']
    robot = dict()
    robot['battle_id'] = fake.random_int(min=1111, max=9999)
    robot['direction'] = allowed_directions[fake.random_int(min=0, max=3)]
    robot['position'] = fake.word()

    # when
    model = models.RobotSchema()
    result = model.load(robot)

    # then
    assert 'position' not in result.data
    assert result.errors['position'][0] == 'Not a valid list.'


def test_should_refuse_any_id_length_rather_than_4():
    """Validate ID length.

    This test will try to insert an integer ID, but with a length different
    from 4 and check if our model refuses it.

    """
    # given
    fake = Faker()
    fake.provider('address')
    allowed_directions = ['north', 'south', 'west', 'east']

    a_id = fake.random_int(min=111, max=999)
    b_id = fake.random_int(min=11111, max=99999)

    a_robot = dict()
    a_robot['battle_id'] = a_id
    a_robot['direction'] = allowed_directions[fake.random_int(min=0, max=3)]
    a_robot['position'] = [fake.random_int(min=1, max=9), fake.random_int(min=1, max=9)]

    b_robot = dict()
    b_robot['battle_id'] = b_id
    b_robot['direction'] = allowed_directions[fake.random_int(min=0, max=3)]
    b_robot['position'] = [fake.random_int(min=1, max=9), fake.random_int(min=1, max=9)]

    # when
    a_model = models.RobotSchema()
    a_result = a_model.load(a_robot)

    b_model = models.RobotSchema()
    b_result = b_model.load(b_robot)

    # then
    assert 'battle_id' not in a_result.data
    assert 'battle_id' not in b_result.data

    assert a_result.errors['battle_id'][0] == (f"The battle ID should be "
                                               f"4 digits long.")
    assert b_result.errors['battle_id'][0] == (f"The battle ID should be "
                                               f"4 digits long.")


@patch('dino_extinction.blueprints.robots.models.redis')
def test_raise_error_if_position_isnt_empty(mocked_redis):
    """Refuse taken places.

    This test will try to create a new robot in a already taken place
    and it will pass if the function raises an error.

    ...

    Parameters
    ----------
    mocked_redis : magic mock
        The mock of our Redis module.

    """
    # given
    fake = Faker()
    fake.provider('address')
    allowed_directions = ['north', 'south', 'west', 'east']
    id = fake.random_int(min=1111, max=9999)
    direction = allowed_directions[fake.random_int(min=0, max=3)]
    position = [fake.random_int(min=1, max=9), fake.random_int(min=1, max=9)]

    state = [[None] * 9 for _ in range(10)]
    state[position[0] - 1][position[1] - 1] = fake.word()

    board = dict()
    board.setdefault('state', state)

    battle = dict()
    battle.setdefault('board', board)

    pickled_battle = pickle.dumps(battle)
    mocked_redis.instance.get.return_value = pickled_battle

    robot = dict()
    robot['battle_id'] = id
    robot['direction'] = direction
    robot['position'] = position

    # when
    model = models.RobotSchema()
    result = model.load(robot)

    # then
    assert result.errors['_schema'][0] == 'This position is not empty'
    mocked_redis.instance.set.assert_not_called()


@patch('dino_extinction.blueprints.robots.models.redis')
def test_raise_error_if_position_is_out_of_range(mocked_redis):
    """Refuse positions that is out of range.

    This test will try to create a new robot with a position out of
    range. It will succeed if it raises an error.

    ...

    Parameters
    ----------
    mocked_redis : magic mock
        The mock of our Redis module.

    """
    # given
    fake = Faker()
    fake.provider('address')
    allowed_directions = ['north', 'south', 'west', 'east']
    id = fake.random_int(min=1111, max=9999)
    direction = allowed_directions[fake.random_int(min=0, max=3)]
    position = [fake.random_int(min=10, max=9999), fake.random_int(min=10, max=9999)]

    state = [[None] * 9 for _ in range(9)]

    board = dict()
    board.setdefault('state', state)

    battle = dict()
    battle.setdefault('board', board)

    pickled_battle = pickle.dumps(battle)
    mocked_redis.instance.get.return_value = pickled_battle

    robot = dict()
    robot['battle_id'] = id
    robot['direction'] = direction
    robot['position'] = position

    # when
    model = models.RobotSchema()
    result = model.load(robot)

    # then
    assert result.errors['_schema'][0] == 'This position is out of range'
    mocked_redis.instance.set.assert_not_called()


@patch('dino_extinction.blueprints.robots.models.redis')
def test_raise_error_if_position_misses_x_or_y(mocked_redis):
    """Refuse positions X or Y is missing.

    This test will try to create a new robot with a missing position at X or Y
    and it should not accept that.

    Parameters
    ----------
    mocked_redis : magic mock
        The mock of our Redis module.

    """
    # given
    fake = Faker()
    fake.provider('address')
    allowed_directions = ['north', 'south', 'west', 'east']
    id = fake.random_int(min=1111, max=9999)
    direction = allowed_directions[fake.random_int(min=0, max=3)]
    position = [fake.random_int(min=10, max=9999)]

    state = [[None] * 9 for _ in range(9)]

    board = dict()
    board.setdefault('state', state)

    battle = dict()
    battle.setdefault('board', board)

    pickled_battle = pickle.dumps(battle)
    mocked_redis.instance.get.return_value = pickled_battle

    robot = dict()
    robot['battle_id'] = id
    robot['direction'] = direction
    robot['position'] = position

    # when
    model = models.RobotSchema()
    result = model.load(robot)

    # then
    assert result.errors['position'][0] == 'You must provide xPos and yPos'
    mocked_redis.instance.set.assert_not_called()


@patch('dino_extinction.blueprints.robots.models.redis')
def test_raise_if_direction_is_not_allowed(mocked_redis):
    """Refuse not allowed directions.

    This test will try to create a new robot using a not allowed direction.
    Allowed directions are: north, south, west and east

    Parameters
    ----------
    mocked_redis : magic mock
        The mock of our Redis module.

    """
    # given
    fake = Faker()
    fake.provider('address')
    id = fake.random_int(min=1111, max=9999)
    direction = fake.word()
    position = [fake.random_int(min=10, max=9999)]

    state = [[None] * 9 for _ in range(9)]

    board = dict()
    board.setdefault('state', state)

    battle = dict()
    battle.setdefault('board', board)

    pickled_battle = pickle.dumps(battle)
    mocked_redis.instance.get.return_value = pickled_battle

    robot = dict()
    robot['battle_id'] = id
    robot['direction'] = direction
    robot['position'] = position

    # when
    model = models.RobotSchema()
    result = model.load(robot)

    # then
    assert result.errors['direction'][0] == 'The direction must be north, south, west or east'
    mocked_redis.instance.set.assert_not_called()


def test_change_the_direction_of_a_robot():
    """Change the direction of a robot.

    This test will try to change the direction of a robot, in a random
    scenario, and it will pass if it works properly. The idea is to turn
    counterclockwise in cardinal points if it wants to turn-left and clockwise
    if it wants to turn right.

    """
    # given
    fake = Faker()

    left_previous_directions = ['north', 'east', 'south', 'west']
    left_new_directions = ['west', 'north', 'east', 'south']
    left_picked_direction = random.choice(left_previous_directions)
    left_choosed_index = left_previous_directions.index(left_picked_direction)
    left_expected_answer = left_new_directions[left_choosed_index]

    right_previous_directions = ['north', 'east', 'south', 'west']
    right_new_directions = ['east', 'south', 'west', 'north']
    right_picked_direction = random.choice(right_previous_directions)
    right_choosed_index = right_previous_directions.index(right_picked_direction)
    right_expected_answer = right_new_directions[right_choosed_index]

    # when
    model = models.RobotSchema()

    left_result = model.change_direction(left_picked_direction, 'turn-left')
    right_result = model.change_direction(right_picked_direction, 'turn-right')

    # then
    assert left_result == left_expected_answer
    assert right_result == right_expected_answer


def test_change_the_direction_of_a_robot_last_cardinal():
    """Change the direction of a robot on the last cardinal point.

    This test will try to change the direction of a robot and check if it
    works, but it will always test the last cardinal point.

    """
    # given
    fake = Faker()

    left_previous_directions = ['north', 'east', 'south', 'west']
    left_new_directions = ['west', 'north', 'east', 'south']
    left_picked_direction = 'east'
    left_choosed_index = left_previous_directions.index(left_picked_direction)
    left_expected_answer = left_new_directions[left_choosed_index]

    right_previous_directions = ['north', 'east', 'south', 'west']
    right_new_directions = ['east', 'south', 'west', 'north']
    right_picked_direction = 'west'
    right_choosed_index = right_previous_directions.index(right_picked_direction)
    right_expected_answer = right_new_directions[right_choosed_index]

    # when
    model = models.RobotSchema()

    left_result = model.change_direction(left_picked_direction, 'turn-left')
    right_result = model.change_direction(right_picked_direction, 'turn-right')

    # then
    assert left_result == left_expected_answer
    assert right_result == right_expected_answer
