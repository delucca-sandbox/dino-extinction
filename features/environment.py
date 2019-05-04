import yaml

from behave import fixture
from behave import use_fixture
from dino_extinction import create_app


@fixture
def flask_client(context, *args, **kwargs):
    app = create_app(config='test')
    app.testing = True
    
    context.client = app.test_client()


def before_all(context):
    config = open('dino_extinction/config.yaml', 'r')
    context.config = yaml.safe_load(config)['test']

    use_fixture(flask_client, context)
