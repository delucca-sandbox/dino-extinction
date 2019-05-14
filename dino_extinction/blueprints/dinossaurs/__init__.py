"""Battles Blueprint.

This module will initialize the Battles Blueprint. Creating the
Blueprint, setting it up and also creating it's routes.

"""
from flask import Blueprint
from . import routes
from . import handlers

bp = Blueprint('dinossaurs', __name__)
routes.set_routes(bp, handlers)
