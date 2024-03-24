from flask import abort, session, request
from functools import wraps


def login_required(role):
    """Decorator to check whether the user is logged in and the access level of the user"""

    def outer_wrapper(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # check if the user is logged in or not
            if not session:
                abort(401, "Access Denied. Please log in to access this resource!")

            # if logged in check the role of the user
            if session.get("role") != role:
                abort(403, "Access Denied. You do not have the proper access level!")

            return f(*args, **kwargs)

        return wrapper

    return outer_wrapper


# not required anymore this behaviour can be handled by the frontend
def if_logged_in(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session:
            if session["role"] != request.endpoint.split("_")[0]:
                abort(403, "Access Denied. You do not have the proper access level!")
            if session["role"] == request.endpoint.split("_")[0]:
                abort(400, "You are already logged in!")
        return f(*args, **kwargs)

    return wrapper
