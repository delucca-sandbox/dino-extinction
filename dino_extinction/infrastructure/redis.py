from flask_redis import FlaskRedis

instance = FlaskRedis()


def bind(app):
    instance.init_app(app)

    return True
