from . import auth
from ..extensions import db
from ..models import LoginAttempts
from datetime import datetime


def update_login_attempt(user_uuid, success):
    if user_uuid:
        attempt = LoginAttempts.query.filter_by(login_uuid=user_uuid).first()
        if not attempt:
            attempt = LoginAttempts(login_uuid=user_uuid, last_login=datetime.now(), failed_login_attempts=0)
            db.session.add(attempt)

        attempt.last_login = datetime.now()
        if not success:
            attempt.failed_login_attempts += 1
        else:
            attempt.failed_login_attempts = 0  # Reset on successful login

        db.session.commit()