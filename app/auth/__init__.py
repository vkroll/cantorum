from flask import Blueprint

auth= Blueprint('auth', __name__)

from . import routes  # Importing routes at the end to avoid circular dependencies
