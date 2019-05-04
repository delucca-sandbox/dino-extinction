from flask import Blueprint

bp = Blueprint('battle', __name__)

from . import routes
