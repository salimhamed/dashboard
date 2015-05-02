from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


def permission_required(permission):
    """
    Takes a permission function as an argument and returns a decorated
    function.
    """
    def decorator(f):
        @wraps(f)  # wraps keeps the name and docstring of the decorated func
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
