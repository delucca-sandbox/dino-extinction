import json

from behave import *
from dino_extinction.infrastructure import redis


@given('a valid request')
def step_impl(context):
    context.params = {}


@when('we create a new battlefield')
def step_impl(context):
    context.response = context.client.post('/battle/new',
                                           data=context.params,
                                           follow_redirects=True)

    assert context.response


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
