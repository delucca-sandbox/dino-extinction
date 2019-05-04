import json

from flask import Response
from . import bp
from . import handlers


@bp.route('/new', methods=['POST'])
def index():
    data = handlers.new_battlefield()
    response = json.dumps(data)

    return Response(response, mimetype='application/json')
