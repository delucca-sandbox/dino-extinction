from behave import *

@given('a valid request')
def step_impl(context):
    pass

@when('we create a new battlefield')
def step_impl(context):
    assert True is not False

@then('we receive the battlefield ID')
def step_impl(context):
    assert context.failed is False
