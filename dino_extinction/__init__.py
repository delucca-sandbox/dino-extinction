import yaml

from flask import Flask
from flask_script import Manager
from dino_extinction.infrastructure import redis


def load_configs(env):
    return yaml.safe_load(open('dino_extinction/config.yaml'))[env]


def create_app(env='DEVELOPMENT'):
    app = Flask(__name__)

    custom_configs = load_configs(env)
    app.config = { **app.config, **custom_configs }

    with app.app_context():
        redis.bind(app)

        from dino_extinction.blueprints import healthcheck
        from dino_extinction.blueprints import battle

        app.register_blueprint(healthcheck.bp, url_prefix='/healthcheck')
        app.register_blueprint(battle.bp, url_prefix='/battle')

        return app

manager = Manager(create_app)
manager.add_option('-e', '--env', dest='env', required=False)

if __name__ == '__main__':
    manager.run(port=config.port)
