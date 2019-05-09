"""Dino Extinction API.

This module is responsible for starting the Dino Extinction API. It will
setup the entire API and create the Flask APP that it will run into our
entire application.

"""
import yaml

from flask import Flask
from flask_script import Manager
from dino_extinction.infrastructure import redis


def load_configs(env):
    """Load a specific environment configuration.

    This function loads the configuration of a specific environment from our
    config yaml file.

    ...

    Parameters
    ----------
    env : string
        The environment that you want to load the configs from.

    """
    return yaml.safe_load(open('dino_extinction/config.yaml'))[env]


def create_app(env='DEVELOPMENT'):
    """Create a Flask app into a given environment.

    This function creates a new Flask application in a given environment
    in order to start our API.

    ...

    Parameters
    ----------
    env : string
        The environment where you want to start the current app.

    """
    app = Flask(__name__)

    custom_configs = load_configs(env)
    app.config = {**app.config, **custom_configs}

    with app.app_context():
        redis.bind(app)

        from dino_extinction.blueprints import healthcheck
        from dino_extinction.blueprints import battle

        app.register_blueprint(healthcheck.bp, url_prefix='/healthcheck')
        app.register_blueprint(battle.bp, url_prefix='/battle')

        return app


manager = Manager(create_app)
manager.add_option('-e', '--env', dest='env', required=False)
