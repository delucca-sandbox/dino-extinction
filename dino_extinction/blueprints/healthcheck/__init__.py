"""Healthcheck Blueprint.

This module will initialize the Healthcheck Blueprint. Creating the
Blueprint, setting it up and also creating it's routes.

"""
from flask import Blueprint
from . import routes

bp = Blueprint('healthcheck', __name__)
routes.set_routes(bp)
