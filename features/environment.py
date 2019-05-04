import yaml
import fakeredis

from behave import fixture
from behave import use_fixture
from dino_extinction import create_app
from dino_extinction.infrastructure import redis


@fixture
def flask_client(context, *args, **kwargs):
    app = create_app(env='TESTING')
    app.testing = True

    fake_redis = fakeredis.FakeServer()
    redis.instance = fakeredis.FakeStrictRedis(server=fake_redis)

    context.client = app.test_client()


def before_all(context):
    use_fixture(flask_client, context)
