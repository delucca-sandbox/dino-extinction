"""Robots API routes.

This module is responsible for creating our API routes for our Robots
service. We're using our Robots Blueprint to do so.

Prefix: /robots

"""
import json

from flask import (Response, request)


def set_routes(bp, handlers):
    """Set the routes for our Robots Blueprint.

    This function sets the routes for our Robots Blueprint. It will
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
    def route_new():
        battle_id = request.values.get('battleId')
        direction = request.values.get('direction')
        board_position = (request.values.get('yPosition'),
                          request.values.get('xPosition'))

        errors, _ = handlers.new_robot(battle_id=battle_id,
                                       direction=direction,
                                       board_position=board_position)
        parsed = json.dumps(False if errors else 'Robot created')
        status = 500 if errors else 200
        mimetype = 'application/json'

        return Response(parsed,
                        status=status,
                        mimetype=mimetype)

    @bp.route('/command', methods=['POST'])
    def route_command():
        mimetype = 'application/json'
        status = dict()
        status.setdefault('error', 500)
        status.setdefault('success', 200)

        battle_id = request.values.get('battleId')
        robot_id = request.values.get('robot')
        action = request.values.get('action')

        robot_pattern = 'R-'
        if robot_id[:2] != robot_pattern:
            return Response(False,
                            status=status.get('error'),
                            mimetype=mimetype)

        errors, _ = handlers.command_robot(battle_id=battle_id,
                                           robot_id=robot_id,
                                           action=action)
        parsed = json.dumps(False if errors else 'Robot commanded')
        status = status.get('error') if errors else status.get('success')

        return Response(parsed,
                        status=status,
                        mimetype=mimetype)
