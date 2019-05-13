"""Dinossaurs API routes.

This module is responsible for creating our API routes for our Dinossaurs
service. We're using our Dinossaurs Blueprint to do so.

Prefix: /dinossaurs

"""
import json

from flask import (Response, request)


def set_routes(bp, handlers):
    """Set the routes for our Dinossaurs Blueprint.

    This function sets the routes for our Dinossaurs Blueprint. It will
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
        battle_id = request.values.get('battleId')
        board_position = (request.values.get('xPosition'),
                          request.values.get('yPosition'))

        errors, data = handlers.new_dinossaur(battle_id=battle_id,
                                              board_position=board_position)
        parsed = json.dumps(False if errors else data)
        status = 500 if errors else 200
        mimetype = 'application/json'

        return Response(parsed,
                        status=status,
                        mimetype=mimetype)
