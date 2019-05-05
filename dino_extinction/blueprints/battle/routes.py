import json

from flask import Response
from . import bp
from . import handlers


@bp.route('/new', methods=['POST'])
def index():
    errors, battle = handlers.new_battlefield()
    parsed = json.dumps(False if errors else battle)
    status = 500 if errors else 200
    mimetype = 'application/json'

    return Response(parsed,
                    status=status,
                    mimetype=mimetype)
