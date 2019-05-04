import json

from flask import Response
from dino_extinction.healthcheck import bp

@bp.route('/')
def index():
    response = {
        'status': 'pass'
    }
    healthcheck = json.dumps(response)

    return Response(healthcheck, mimetype='application/health+json')
