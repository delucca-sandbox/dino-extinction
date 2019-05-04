from behave import *


@given('a empty request to healthcheck')
def step_impl(context):
    context.response = context.client.get('/healthcheck', follow_redirects=True)

    assert context.response


@then('should receive a 200 status')
def step_impl(context):
    assert context.response.status_code == 200
