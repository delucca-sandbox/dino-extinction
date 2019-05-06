import json

from flask import (Response, request)
from . import bp
from . import handlers


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
