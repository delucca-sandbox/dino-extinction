"""Dinossaurs Blueprint.

This module will initialize the Dinossaurs Blueprint. Creating the
Blueprint, setting it up and also creating it's routes.

"""
from flask import Blueprint
from . import routes
from . import handlers

bp = Blueprint('battles', __name__)
routes.set_routes(bp, handlers)
