"""Battle Models Unit Tests.

This test file will ensure that the most important logic of our Battle
blueprint's models are working as we are expecting.

"""
import pickle

from faker import Faker
from mock import patch
from dino_extinction.blueprints.battles import models


def test_generate_battle_model():
    """Test the creation of a new battle.

    This test will try to create a new battle based on our model and ensure
    that it is working properly.

    """
    # given
    fake = Faker()
    fake.provider('address')
    digits = [str(fake.random_digit()) for _ in range(4)]
    id = int(''.join(digits))
    board_size = fake.random_digit()

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
    """Test ID validation of type.

    This test will try to insert an invalid ID data and check if our model
    is refusing any inputs that are not integers.

    """
    # given
    fake = Faker()
    fake.provider('python')
    battle = dict()
    battle['id'] = fake.word()
    battle['board_size'] = fake.random_digit()

    # when
    model = models.BattleSchema()
    result = model.load(battle)

    # then
    assert 'id' not in result.data
    assert result.errors['id'][0] == 'Not a valid integer.'


def test_should_refuse_any_id_length_rather_than_4():
    """Test ID validation of length.

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

    a_battle = dict()
    a_battle['id'] = a_id
    a_battle['board_size'] = fake.random_digit()

    b_battle = dict()
    b_battle['id'] = b_id
    b_battle['board_size'] = fake.random_digit()

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
    """Test a new battle creation.

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
    digits = [str(fake.random_digit()) for _ in range(4)]
    id = int(''.join(digits))
    board_size = fake.random_digit()

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
