import json

from flask import Response
from . import bp


@bp.route('/', methods=['GET'])
def index():
    response = dict()
    response['status'] = 'pass'
    healthcheck = json.dumps(response)
    mimetype = 'application/health+json'

    return Response(healthcheck, mimetype=mimetype)
