"""Battle API routes.

This module is responsible for creating our API routes for our Battle
service. We're using our Battle Blueprint to do so.

Prefix: /battle

"""
import json

from flask import (Response, request)


def set_routes(bp, handlers):
    """Set the routes for our Battle Blueprint.

    This function sets the routes for our Battle Blueprint. It will
    start every route that is specified inside of this function.

    ...

    Parameters
    ----------
    bp : flask blueprint
        A Flask Blueprint that will receive all routes.

    handlers : module
        The handlers for our current module.

    """
    @bp.route('/new', methods=['POST'])
    def index():
        board_size = request.values.get('size') or 50
        errors, battle = handlers.new_battlefield(board_size=board_size)
        parsed = json.dumps(False if errors else battle)
        status = 500 if errors else 200
        mimetype = 'application/json'

        return Response(parsed,
                        status=status,
                        mimetype=mimetype)
