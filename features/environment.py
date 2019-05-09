"""Behave Environment Configuration.

This module configures the Behave environment, setting some fixtures and
also setting up everything that must run on the test lifecycle.

"""
import fakeredis

from behave import fixture
from behave import use_fixture
from dino_extinction import create_app
from dino_extinction.infrastructure import redis


@fixture
def flask_client(context, *args, **kwargs):
    """Start a new Flask Test Client.

    This fixture will start a new Flask Client, also configuring it to
    run as test in order to make it easier to run our requests on it.

    """
    app = create_app(env='TESTING')
    app.testing = True

    fake_redis = fakeredis.FakeServer()
    redis.instance = fakeredis.FakeStrictRedis(server=fake_redis)

    context.client = app.test_client()


def before_all(context):
    """Execute some actions before all features.

    This lifecycle method will execute a series of actions and functions
    before any feature runs.

    """
    use_fixture(flask_client, context)
