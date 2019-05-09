"""Healthcheck API routes.

This module is responsible for creating our API routes for our Healthcheck
service. We're using our Healthcheck Blueprint to do so.

Prefix: /healthcheck

"""
import json

from flask import Response


def set_routes(bp):
    """Set the routes for our Healthcheck Blueprint.

    This function sets the routes for our Healthcheck Blueprint. It will
    start every route that is specified inside of this function.

    ...

    Parameters
    ----------
    bp : flask blueprint
        A Flask Blueprint that will receive all routes.

    """
    @bp.route('/', methods=['GET'])
    def index():
        """Create the index route.

        This route is responsible for all incoming GET requests into our
        /healthcheck route.

        """
        response = dict()
        response['status'] = 'pass'
        healthcheck = json.dumps(response)
        mimetype = 'application/health+json'

        return Response(healthcheck, mimetype=mimetype)
