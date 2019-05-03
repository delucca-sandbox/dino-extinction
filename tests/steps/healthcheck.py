from behave import *

import requests

@given('a empty request to healthcheck')
def step_impl(context):
    config = context.config

    url = '{}/healthcheck'.format(config['server']['url'])
    context.res = requests.get(url)

@then('should receive a 200 status')
def step_impl(context):
    assert context.res.status_code == 200
