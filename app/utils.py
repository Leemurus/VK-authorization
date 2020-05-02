from functools import wraps

from flask import request, current_app
from flask_login import current_user
from flask_login.config import EXEMPT_METHODS


def not_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)

    return wrapper
