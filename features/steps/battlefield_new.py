from behave import *


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
    assert context.response.data.id
