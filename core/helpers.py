from .student import Student


def before_request(f):
    """Decorator to check if students are present"""

    def wrapper(*agrs, **kwargs):
        # check if students are present
        if not Student.student_list():
            return " ", 204
        return f(*agrs, **kwargs)

    return wrapper
