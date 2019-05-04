import json

from flask import Response
from . import bp


@bp.route('/', methods=['GET'])
def index():
    response = {
        'status': 'pass'
    }
    healthcheck = json.dumps(response)

    return Response(healthcheck, mimetype='application/health+json')
