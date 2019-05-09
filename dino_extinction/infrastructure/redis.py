"""Redis Integration.

This module integrates with Redis using FlaskRedis.

"""
from flask_redis import FlaskRedis

instance = FlaskRedis()


def bind(app):
    """Bind a FlaskRedis instance into your app.

    This function binds a FlaskRedis instance with your current app. In
    other to do so, first create your Flask app and them pass it to this
    function.

    ...

    Parameters
    ----------
    app : class
        Your Flask application.

    """
    instance.init_app(app)

    return True
