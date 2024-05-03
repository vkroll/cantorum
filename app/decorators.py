# decorators.py

from functools import wraps
from flask import abort
from flask_login import current_user

def role_required(*roles):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_user.is_authenticated and current_user.has_any_role(*roles):
                return func(*args, **kwargs)
            else:
                abort(403)  # HTTP status code for forbidden access
        return decorated_view
    return wrapper