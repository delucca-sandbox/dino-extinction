"""Robots Routes Unit Tests.

This test file will ensure that the most important logic of our Robots
blueprint routes are working as we are expecting.

"""
import json

from mock import (patch, MagicMock)
from faker import Faker
from dino_extinction.blueprints.robots import routes


@patch('dino_extinction.blueprints.robots.routes.Response')
@patch('dino_extinction.blueprints.robots.routes.request')
def test_invalid_robot_id(mocked_request, mocked_response):
    """Refuse invalid robot IDs

    This test will ensure that if we provide an invalid robot ID (not
    starting with "R-") our route will refuse it

    ...

    Parameters
    ----------
    mocked_request : magic mock
        The mock of our Flask request object.

    mocked_response : magic mock
        The mock of our Flask response Class.

    """
    class FakeDecorator:
        def route(route, methods=[]):
            def wrapper(fnc):
                if route == '/command':
                    fnc()

            return wrapper

    # given
    fake = Faker()
    robot_id = fake.word()
    values = dict()
    values.setdefault('robot', robot_id)
    mocked_request.values = values

    mocked_handlers = MagicMock()
    mocked_handlers.command_robot.return_value = (fake.word(), fake.word())

    # when
    routes.set_routes(FakeDecorator, mocked_handlers)

    # then
    mocked_handlers.command_robot.assert_not_called()
    mocked_response.assert_called_once_with(json.dumps(False),
                                            status=500,
                                            mimetype='application/json')
