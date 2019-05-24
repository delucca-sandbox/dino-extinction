"""Battles API routes.

This module is responsible for creating our API routes for our Battle
service. We're using our Battles Blueprint to do so.

Prefix: /battles

"""
import json

from flask import (Response, request, render_template)
from dino_extinction.blueprints.battles.models import BattleSchema


def set_routes(bp, handlers):
    """Set the routes for our Battles Blueprint.

    This function sets the routes for our Battles Blueprint. It will
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
        board_size = request.values.get('size') or 50
        errors, battle = handlers.new_battle(board_size=board_size)
        parsed = json.dumps(False if errors else battle)
        status = 500 if errors else 200
        mimetype = 'application/json'

        return Response(parsed,
                        status=status,
                        mimetype=mimetype)

    @bp.route('/state', methods=['GET'])
    def route_state():
        battle_id = request.args.get('battleId')
        if not battle_id:
            return _not_found()

        battle_model = BattleSchema()
        page_title = 'Battle Status'
        battle = battle_model.get_battle(battle_id=battle_id)
        if not battle:
            return _not_found()

        return render_template('state.html',
                               title=page_title)

    def _not_found():
        return Response('', status=404)
