from flask import Blueprint

user= Blueprint('user', __name__)

from . import routes  # Importing routes at the end to avoid circular dependencies
