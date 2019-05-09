"""Battle Blueprint.

This module will initialize the Battle Blueprint. Creating the
Blueprint, setting it up and also creating it's routes.

"""
from flask import Blueprint
from . import routes
from . import handlers

bp = Blueprint('battle', __name__)
routes.set_routes(bp, handlers)
