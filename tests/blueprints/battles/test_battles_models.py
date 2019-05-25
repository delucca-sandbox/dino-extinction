"""Battle Models Unit Tests.

This test file will ensure that the most important logic of our Battle
blueprint models are working as we are expecting.

"""
import pickle
import random

from faker import Faker
from mock import patch
from copy import deepcopy
from dino_extinction.blueprints.battles import models


def test_generate_battle_model():
    """Create a new battle.

    This test will try to create a new battle based on our model and ensure
    that it is working properly.

    """
    # given
    fake = Faker()
    fake.provider('address')
    digits = [str(fake.random_int(min=1, max=9)) for _ in range(4)]
    id = int(''.join(digits))
    board_size = fake.random_int(min=1, max=9)

    battle = dict()
    battle['id'] = id
    battle['board_size'] = board_size

    # when
    model = models.BattleSchema()
    result = model.load(battle)

    # then
    assert result.data['id'] == id
    assert result.data['board_size'] == board_size


def test_id_must_be_int():
    """Validate ID type.

    This test will try to insert an invalid ID data and check if our model
    is refusing any inputs that are not integers.

    """
    # given
    fake = Faker()
    fake.provider('python')
    battle = dict()
    battle['id'] = fake.word()
    battle['board_size'] = fake.random_int(min=1, max=9)

    # when
    model = models.BattleSchema()
    result = model.load(battle)

    # then
    assert 'id' not in result.data
    assert result.errors['id'][0] == 'Not a valid integer.'


def test_should_refuse_any_id_length_rather_than_4():
    """Validate ID length.

    This test will try to insert an integer ID, but with a length different
    from 4 and check if our model refuses it.

    """
    # given
    fake = Faker()
    fake.provider('address')

    a_digits = [str(fake.random_int(min=1, max=9)) for _ in range(3)]
    a_id = int(''.join(a_digits))

    b_digits = [str(fake.random_int(min=1, max=9)) for _ in range(5)]
    b_id = int(''.join(b_digits))

    a_battle = dict()
    a_battle['id'] = a_id
    a_battle['board_size'] = fake.random_int(min=1, max=9)

    b_battle = dict()
    b_battle['id'] = b_id
    b_battle['board_size'] = fake.random_int(min=1, max=9)

    # when
    a_model = models.BattleSchema()
    a_result = a_model.load(a_battle)

    b_model = models.BattleSchema()
    b_result = b_model.load(b_battle)

    # then
    assert 'id' not in a_result.data
    assert 'id' not in b_result.data

    assert a_result.errors['id'][0] == 'The battle ID should be 4 digits long.'
    assert b_result.errors['id'][0] == 'The battle ID should be 4 digits long.'


@patch('dino_extinction.blueprints.battles.models.redis')
def test_create_new_battle(mocked_redis):
    """New battle creation.

    This test will try to create a new battle and check if it is inserting
    the data in our Redis instance.

    ...

    Parameters
    ----------
    mocked_redis : magic mock
        The mock of our Redis module.

    """
    # given
    fake = Faker()
    fake.provider('address')
    digits = [str(fake.random_int(min=1, max=9)) for _ in range(4)]
    id = int(''.join(digits))
    board_size = fake.random_int(min=1, max=9)

    battle = dict()
    battle['id'] = id
    battle['board_size'] = board_size

    # when
    model = models.BattleSchema()

    model.dumps(battle)

    # then
    expected_board = dict()
    expected_board['size'] = board_size
    expected_board['state'] = [[None] * board_size for _ in range(board_size)]

    expected_battle = dict()
    expected_battle['board'] = expected_board

    pickled_expected_battle = pickle.dumps(expected_battle)

    assert mocked_redis.instance.set.call_count == 1
    mocked_redis.instance.set.assert_called_with(id, pickled_expected_battle)


@patch('dino_extinction.blueprints.battles.models.redis')
@patch('dino_extinction.blueprints.battles.models.pickle')
def test_get_battle(mocked_pickle, mocked_redis):
    """Get an existing battle.

    This test will try to get an existing battle and it will pass if our model
    returns that battle for us.

    ...

    Parameters
    ----------
    mocked_pickle: magic mock
        The mock of the Pickle library.

    mocked_redis : magic mock
        The mock of our Redis module.

    """
    # given
    fake = Faker()
    battle_id = fake.word()
    expected_return = fake.word()
    mocked_redis.instance.get.return_value = expected_return
    mocked_pickle.loads.return_value = expected_return

    # when
    model = models.BattleSchema()
    result = model.get_battle(battle_id)

    # then
    assert result == expected_return
    assert mocked_redis.instance.get.call_count == 1
    mocked_redis.instance.get.assert_called_with(battle_id)


@patch('dino_extinction.blueprints.battles.models.redis')
@patch('dino_extinction.blueprints.battles.models.pickle')
def test_not_get_unknow_battle(mocked_pickle, mocked_redis):
    """Ignore an unknow battle.

    This test will try to get an unknow battle and it should pass if the
    result to that was None.

    ...

    Parameters
    ----------
    mocked_pickle: magic mock
        The mock of the Pickle library.

    mocked_redis : magic mock
        The mock of our Redis module.

    """
    # given
    fake = Faker()
    mocked_redis.instance.get.return_value = None

    # when
    model = models.BattleSchema()
    result = model.get_battle(fake.word())

    # then
    mocked_pickle.loads.assert_not_called()

    assert not result
    assert mocked_redis.instance.get.call_count == 1


@patch('dino_extinction.blueprints.battles.models.redis')
@patch('dino_extinction.blueprints.battles.models.pickle')
def test_get_battle_serializing_pickle_data(mocked_pickle, mocked_redis):
    """Normalize battle data.

    This test will try to get an existing battle and it should pass if it
    send the right data to pickle and return to us the loaded pickle data.

    ...

    Parameters
    ----------
    mocked_pickle: magic mock
        The mock of the Pickle library.

    mocked_redis : magic mock
        The mock of our Redis module.

    """
    # given
    fake = Faker()
    battle_id = fake.word()
    raw_data = fake.word()
    expected_return = fake.word()
    mocked_redis.instance.get.return_value = raw_data
    mocked_pickle.loads.return_value = expected_return

    # when
    model = models.BattleSchema()
    result = model.get_battle(battle_id)

    # then
    assert result == expected_return
    assert result != raw_data
    assert mocked_pickle.loads.call_count == 1
    mocked_pickle.loads.assert_called_with(raw_data)


@patch('dino_extinction.blueprints.battles.models.redis')
def test_update_battle(mocked_redis):
    """Update a battle data.

    This test will try to update a battle with a new data and it will pass
    if it sends the data pickled to Redis.

    ...

    Parameters
    ----------
    mocked_redis : magic mock
        The mock of our Redis module.

    """
    # given
    fake = Faker()
    battle_id = fake.word()
    new_clean_data = fake.word()
    new_raw_data = pickle.dumps(new_clean_data)

    # when
    model = models.BattleSchema()
    model.update_battle(battle_id, new_clean_data)

    # then
    assert mocked_redis.instance.set.call_count == 1
    mocked_redis.instance.set.assert_called_with(battle_id, new_raw_data)


def test_robot_move():
    """Move a robot inside the battlefield.

    This test will try to move a robot in the battlefield. It should pass if
    it returns the robot moved according to the action, changing it's position
    on the battlefield and also it's position inside the entities.

    """
    def _find_new_robot_spot(action):
        return (2, 3) if action == 'move-forward' else (4, 3)

    # given
    fake = Faker()
    robot_id = fake.word()
    options = ['move-forward', 'move-backwards']
    action = random.choice(options)
    default_size = 9
    default_board = [[None] * default_size for _ in range(default_size)]

    robot = dict()
    robot.setdefault('direction', 'north')
    robot.setdefault('position', (3, 3))
    board_with_robot = deepcopy(default_board)
    board_with_robot[2][2] = robot_id

    entities = dict()
    entities.setdefault(robot_id, robot)

    board = dict()
    board.setdefault('size', default_size)
    board.setdefault('state', board_with_robot)

    battle = dict()
    battle.setdefault('entities', entities)
    battle.setdefault('board', board)

    # when
    model = models.BattleSchema()
    result = model.robot_move(battle, robot_id, action)

    # then
    moved_battle = deepcopy(battle)
    new_robot_position = _find_new_robot_spot(action)
    board_with_moved_robot = deepcopy(default_board)
    board_with_moved_robot[new_robot_position[0] - 1][new_robot_position[1] - 1] = \
        robot_id

    moved_board = dict()
    moved_board.setdefault('state', board_with_moved_robot)

    moved_robot = dict()
    moved_robot.setdefault('position', new_robot_position)

    moved_battle.get('board').update(moved_board)
    moved_battle.get('entities').get(robot_id).update(moved_robot)

    assert result == moved_battle


def test_robot_move_in_a_taken_spot():
    """Move a robot inside the battlefield in a taken spot.

    This test will try to move a robot in the battlefield. It should pass if
    it returns false because there will already be another entity at that
    place.

    """
    # given
    fake = Faker()
    robot_id = fake.word()
    options = ['move-forward', 'move-backwards']
    action = random.choice(options)
    default_size = 9
    default_board = [[None] * default_size for _ in range(default_size)]

    robot = dict()
    robot.setdefault('direction', 'north')
    robot.setdefault('position', (3, 3))
    board_with_robot = deepcopy(default_board)
    board_with_robot[2][2] = robot_id
    board_with_robot[1 if action == 'move-forward' else 3][2] = fake.word()

    entities = dict()
    entities.setdefault(robot_id, robot)

    board = dict()
    board.setdefault('size', default_size)
    board.setdefault('state', board_with_robot)

    battle = dict()
    battle.setdefault('entities', entities)
    battle.setdefault('board', board)

    # when
    model = models.BattleSchema()
    result = model.robot_move(battle, robot_id, action)

    # then
    assert not result


def test_robot_attack():
    """Attack with an robot and destroy all dinossaurs close to it.

    This test will try to attack with a robot and it will pass if we can do so
    and it destroys all dinossaurs close to that robot.

    """
    # given
    fake = Faker()
    robot_id = fake.word()
    default_size = 9
    default_board = [[None] * default_size for _ in range(default_size)]
    default_dino = dict()
    default_dino.setdefault(fake.word(), fake.word())

    robot = dict()
    robot.setdefault('direction', 'north')
    robot.setdefault('position', (3, 3))
    board_with_robot_and_dinos = deepcopy(default_board)
    board_with_robot_and_dinos[2][2] = robot_id
    board_with_robot_and_dinos[3][2] = 'D-1111'
    board_with_robot_and_dinos[3][3] = 'D-2222'

    entities = dict()
    entities.setdefault(robot_id, robot)
    entities.setdefault('D-1111', default_dino)
    entities.setdefault('D-2222', default_dino)

    board = dict()
    board.setdefault('size', default_size)
    board.setdefault('state', board_with_robot_and_dinos)

    battle = dict()
    battle.setdefault('entities', entities)
    battle.setdefault('board', board)

    # when
    model = models.BattleSchema()
    result = model.robot_attack(battle, robot_id)

    # then
    board_with_robot = deepcopy(default_board)
    board_with_robot[2][2] = robot_id

    attacked_entities = dict()
    attacked_entities.setdefault(robot_id, robot)

    attacked_board = dict()
    attacked_board.setdefault('size', default_size)
    attacked_board.setdefault('state', board_with_robot)

    attacked_battle = dict()
    attacked_battle.setdefault('entities', attacked_entities)
    attacked_battle.setdefault('board', attacked_board)

    assert result == attacked_battle
    assert 'D-1111' not in result.get('entities')
    assert 'D-2222' not in result.get('entities')


def test_avoid_friendly_fire():
    """Attack with an robot will not destroy other robots.

    This test will try to attack with a robot and it will test if we will
    not destry any friends.

    """
    # given
    fake = Faker()
    robot_id = fake.word()
    default_size = 9
    default_board = [[None] * default_size for _ in range(default_size)]
    default_robot = dict()
    default_robot.setdefault(fake.word(), fake.word())

    robot = dict()
    robot.setdefault('direction', 'north')
    robot.setdefault('position', (3, 3))
    board_with_robot_and_dinos = deepcopy(default_board)
    board_with_robot_and_dinos[2][2] = robot_id
    board_with_robot_and_dinos[3][2] = 'R-1111'

    entities = dict()
    entities.setdefault(robot_id, robot)
    entities.setdefault('R-1111', default_robot)

    board = dict()
    board.setdefault('size', default_size)
    board.setdefault('state', board_with_robot_and_dinos)

    battle = dict()
    battle.setdefault('entities', entities)
    battle.setdefault('board', board)

    # when
    model = models.BattleSchema()
    result = model.robot_attack(battle, robot_id)

    # then
    assert result == battle
    assert 'R-1111' in result.get('entities')
