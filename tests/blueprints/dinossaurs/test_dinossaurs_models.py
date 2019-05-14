"""Dinossaurs Models Unit Tests.

This test file will ensure that the most important logic of our Dinossaurs
blueprint models are working as we are expecting.

"""
import pickle

from faker import Faker
from mock import patch
from dino_extinction.blueprints.dinossaurs import models


@patch('dino_extinction.blueprints.dinossaurs.models.redis')
def test_generate_dinossaur_model(mocked_redis):
    """Create a new dinossaur.

    This test will try to create a new dinossaur based on our model and ensure
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
    digits = [str(fake.random_digit()) for _ in range(4)]
    id = int(''.join(digits))
    position = [fake.random_digit(), fake.random_digit()]

    state = [[None] * 9 for _ in range(9)]

    board = dict()
    board.setdefault('state', state)

    battle = dict()
    battle.setdefault('board', board)

    pickled_battle = pickle.dumps(battle)
    mocked_redis.instance.get.return_value = pickled_battle

    dinossaur = dict()
    dinossaur['battle_id'] = id
    dinossaur['position'] = position

    # when
    model = models.DinossaurSchema()
    model.dumps(dinossaur)

    # then
    called_id, raw_args = mocked_redis.instance.set.call_args_list[0][0]
    args = pickle.loads(raw_args)
    dino_id = next(iter(args['entities']))
    created_dino = args['entities'][dino_id]

    assert called_id == id
    assert len(args['entities']) == 1
    assert created_dino['type'] == 'DINOSSAUR'
    assert created_dino['position'] == position
    mocked_redis.instance.get.assert_called_once_with(id)


def test_id_must_be_int():
    """Validate ID type.

    This test will try to insert an invalid ID data and check if our model
    is refusing any inputs that are not integers.

    """
    # given
    fake = Faker()
    fake.provider('python')
    dinossaur = dict()
    dinossaur['battle_id'] = fake.word()
    dinossaur['position'] = [fake.random_digit(), fake.random_digit()]

    # when
    model = models.DinossaurSchema()
    result = model.load(dinossaur)

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
    dinossaur = dict()
    dinossaur['battle_id'] = fake.random_digit()
    dinossaur['position'] = fake.word()

    # when
    model = models.DinossaurSchema()
    result = model.load(dinossaur)

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

    a_digits = [str(fake.random_digit()) for _ in range(3)]
    a_id = int(''.join(a_digits))

    b_digits = [str(fake.random_digit()) for _ in range(5)]
    b_id = int(''.join(b_digits))

    a_dinossaur = dict()
    a_dinossaur['battle_id'] = a_id
    a_dinossaur['position'] = [fake.random_digit(), fake.random_digit()]

    b_dinossaur = dict()
    b_dinossaur['battle_id'] = b_id
    b_dinossaur['position'] = [fake.random_digit(), fake.random_digit()]

    # when
    a_model = models.DinossaurSchema()
    a_result = a_model.load(a_dinossaur)

    b_model = models.DinossaurSchema()
    b_result = b_model.load(b_dinossaur)

    # then
    assert 'battle_id' not in a_result.data
    assert 'battle_id' not in b_result.data

    assert a_result.errors['battle_id'][0] == (f"The battle ID should be "
                                               f"4 digits long.")
    assert b_result.errors['battle_id'][0] == (f"The battle ID should be "
                                               f"4 digits long.")


@patch('dino_extinction.blueprints.dinossaurs.models.redis')
def test_raise_error_if_position_isnt_empty(mocked_redis):
    """Refuse taken places.

    This test will try to create a new dinossaur in a already taken place
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
    digits = [str(fake.random_digit()) for _ in range(4)]
    id = int(''.join(digits))
    position = [fake.random_digit(), fake.random_digit()]

    state = [[None] * 9 for _ in range(9)]
    state[position[0]][position[1]] = fake.word()

    board = dict()
    board.setdefault('state', state)

    battle = dict()
    battle.setdefault('board', board)

    pickled_battle = pickle.dumps(battle)
    mocked_redis.instance.get.return_value = pickled_battle

    dinossaur = dict()
    dinossaur['battle_id'] = id
    dinossaur['position'] = position

    # when
    model = models.DinossaurSchema()
    result = model.dumps(dinossaur)

    # then
    assert result.errors['_schema'][0] == 'This position is not empty'
    mocked_redis.instance.set.assert_not_called()
