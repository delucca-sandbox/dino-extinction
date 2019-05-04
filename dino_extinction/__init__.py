from flask import Flask
from flask_script import Manager
from dino_extinction import healthcheck

def create_app(config='dev'):
    app = Flask(__name__)
    app.register_blueprint(healthcheck.bp, url_prefix='/healthcheck')

    return app

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config', required=False)

if __name__ == '__main__':
    manager.run()    
