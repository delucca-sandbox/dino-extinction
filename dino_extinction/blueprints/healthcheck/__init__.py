from flask import Blueprint

bp = Blueprint('healthcheck', __name__)

from . import routes
