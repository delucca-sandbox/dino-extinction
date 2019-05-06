import pickle
import json

from behave import *
from mock import patch
from faker import Faker
from itertools import product
from dino_extinction.infrastructure import redis


@given('a valid request')
def step_impl(context):
    context.params = {}

@given('a valid request asking for 2x2 grid')
def step_impl(context):
    context.params = { 'size': 2 }


@when('we create a new battlefield')
def step_impl(context):
    context.response = context.client.post('/battle/new',
                                           data=context.params,
                                           follow_redirects=True)

    assert context.response


@when('we create an invalid battlefield')
@patch('dino_extinction.blueprints.battle.handlers.randint')
def step_impl(context, mocked_randint):
    fake = Faker()
    battle_id = fake.word()
    mocked_randint.return_value = battle_id

    context.response = context.client.post('/battle/new',
                                           data=context.params,
                                           follow_redirects=True)

    assert context.response

    context.battle_id = battle_id


@then('we receive the battlefield ID')
def step_impl(context):
    assert context.failed is False
    assert context.response.status_code == 200

    response = json.loads(context.response.data.decode('utf-8'))
    assert response['id']

    context.battle_id = response['id']


@then('the battlefield was created')
def step_impl(context):
    assert redis.instance.get(context.battle_id)


@then('we receive an error')
def step_impl(context):
    assert context.failed is False
    assert context.response.status_code == 500

    response = json.loads(context.response.data.decode('utf-8'))


@then('the battlefield was not created')
def step_impl(context):
    assert not redis.instance.get(context.battle_id)


@then('we stored a 2x2 battlefield')
def step_impl(context):
    data = redis.instance.get(context.battle_id)
    battlefield = pickle.loads(data)
    expected_board = {i: x for i, x in enumerate(product(range(2), repeat=2))}

    assert battlefield['board'] == expected_board
