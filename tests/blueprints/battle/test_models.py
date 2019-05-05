from faker import Faker
from mock import patch
from dino_extinction.blueprints.battle import models


def test_generate_battle_model():
    """
    This test ensures that we can generate a valid battle model
    """
    # given
    fake = Faker()
    fake.provider('address')
    digits = [str(fake.random_digit()) for _ in range(4)]
    id = int(''.join(digits))

    battle = dict()
    battle['id'] = id

    # when
    model = models.BattleSchema()
    result = model.load(battle)

    # then
    assert result.data['id'] == id


def test_id_must_be_int():
    """
    This test ensures that our battle only accepts ints
    as theirs ids
    """
    # given
    fake = Faker()
    fake.provider('python')
    battle = dict()
    battle['id'] = fake.word()

    # when
    model = models.BattleSchema()
    result = model.load(battle)

    # then
    assert 'id' not in result.data
    assert result.errors['id'][0] == 'Not a valid integer.'


def test_should_refuse_any_id_length_rather_than_4():
    """
    This test ensures that our model only accepts an id length of 4
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

    b_battle = dict()
    b_battle['id'] = b_id

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


@patch('dino_extinction.blueprints.battle.models.redis')
def test_create_new_battle(mocked_redis):
    """
    This test ensures that we can create a new battle on our model
    """
    # given
    fake = Faker()
    fake.provider('address')
    digits = [str(fake.random_digit()) for _ in range(4)]
    id = int(''.join(digits))

    battle = dict()
    battle['id'] = id

    # when
    model = models.BattleSchema()

    model.dumps(battle)

    # then
    assert mocked_redis.instance.set.call_count == 1
    mocked_redis.instance.set.assert_called_with(id, '{}')
