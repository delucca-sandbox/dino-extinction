from flask import Blueprint

bp = Blueprint('healthcheck', __name__)

from dino_extinction.healthcheck import routes
