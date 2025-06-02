from flask import Blueprint

college = Blueprint("college", __name__, url_prefix='/college')

from . import controller