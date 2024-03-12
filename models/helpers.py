from .student import Student
from functools import wraps
from flask import session, abort


def before_request(f):
    """Decorator to check if students are present"""

    @wraps(f)
    def wrapper(*args, **kwargs):

        if "username" not in session:
            abort(401, "Please Login to accesss")
        # check if students are present
        if not Student.student_list():
            return " ", 204
        return f(*args, **kwargs)

    return wrapper


def login_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            abort(401, "Please Login to access")
        return f(*args, **kwargs)

    return wrapper
