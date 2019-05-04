import json

from flask import Response
from dino_extinction.infrastructure import redis
from . import bp


@bp.route('/new', methods=['POST'])
def index():
    print(redis.instance)
    response = {
        'status': 'pass'
    }
    healthcheck = json.dumps(response)

    return Response(healthcheck, mimetype='application/health+json')
