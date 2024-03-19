from functools import wraps
from flask import abort, session


def login_required(f):
    """Decorator to check if the user if not authenticated"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        # check if the user is logged in or not
        if not session.get("email"):
            abort(401, "Access Denied. Please log in to access this resource")

        return f(*args, **kwargs)

    return wrapper


def if_logged_in(f):
    """Decorator to check if the user is already authenticated"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        # check if the user is already logged in
        if session.get("email"):
            abort(403, "You are already logged in!")

        return f(*args, **kwargs)

    return wrapper
