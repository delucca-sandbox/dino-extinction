"""Healthcheck Steps.

This module contains every step to test the behaviour of our healthcheck
services.

"""
from behave import (given, then)


@given('a empty request to healthcheck')
def step_given_empty_request(context):
    """Generate an empty request.

    This function will generate an empty request to our healthcheck service.

    ...

    Parameters
    ----------
    context : behave context
        The behave context of the current feature test.

    """
    context.response = context.client.get('/healthcheck',
                                          follow_redirects=True)

    assert context.response


@then('should receive a 200 status')
def step_should_receive_200(context):
    """Assert the request succeeded.

    This function will assert that the current request has succeeded.

    ...

    Parameters
    ----------
    context : behave context
        The behave context of the current feature test.

    """
    assert context.response.status_code == 200
