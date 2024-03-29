# app/events/__init__.py

from flask import Blueprint

events = Blueprint('events', __name__)

from . import routes  # Importing routes at the end to avoid circular dependencies
