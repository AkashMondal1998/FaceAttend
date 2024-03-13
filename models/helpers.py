from .student import Student
from functools import wraps
from flask import session, abort


def before_request(f):
    """Decorator to check if students are present"""

    @wraps(f)
    def wrapper(*args, **kwargs):

        # check if the user is logged in or not
        if "username" not in session:
            abort(401, "Access Denied. Please log in to access this resource")

        # check if students are present
        if not Student.student_list():
            return " ", 204

        return f(*args, **kwargs)

    return wrapper


def login_required(f):
    """Decorator to check if the user if logged in"""

    @wraps(f)
    def wrapper(*args, **kwargs):

        # check if the user is logged in or not
        if "username" not in session:
            abort(401, "Access Denied. Please log in to access this resource")

        return f(*args, **kwargs)

    return wrapper
