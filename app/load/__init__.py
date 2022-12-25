from flask import Blueprint

# blue print for authorize
load = Blueprint('load', __name__)

from . import routes