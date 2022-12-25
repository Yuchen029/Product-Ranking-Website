from flask import Blueprint

# blue print for authorize
auth = Blueprint('auth', __name__)

from . import routes