from .student import Student
from functools import wraps


def before_request(f):
    """Decorator to check if students are present"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        # check if students are present
        if not Student.student_list():
            return " ", 204
        return f(*args, **kwargs)

    return wrapper
