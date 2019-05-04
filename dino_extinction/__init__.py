import yaml

from flask import Flask
from flask_script import Manager
from dino_extinction.infrastructure import redis
from dino_extinction.blueprints import healthcheck
from dino_extinction.blueprints import battle


def load_config(env):
    return yaml.load(open('config.yaml')[env])


def create_app(config='dev'):
    print(Flask)
    app = Flask(__name__)
    app.register_blueprint(healthcheck.bp, url_prefix='/healthcheck')
    app.register_blueprint(battle.bp, url_prefix='/battle')

    return app

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config', required=False)

if __name__ == '__main__':
    manager.run(port=config.port)
