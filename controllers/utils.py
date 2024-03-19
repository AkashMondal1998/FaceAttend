from email_validator import validate_email, EmailNotValidError
from flask_restx import fields
from flask import request
import os

UPLOAD_FOLDER = "photos"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def check_email(email):
    """Check if email is valid or not and also checks if the email is deliverable"""

    try:
        email_info = validate_email(email, check_deliverability=True)
    except EmailNotValidError as e:
        return str(e), False
    return email_info.normalized, True


class ImageUrl(fields.Raw):
    """Custom field for student image for the student_model response"""

    def format(self, value):
        return os.path.join(request.url_root, UPLOAD_FOLDER, value)


def allowed_files(filename):
    """Check the extension of file that is being saved"""

    filename = filename.strip()
    file_ext = filename.rsplit(".", 1)[1].lower()
    if file_ext in ALLOWED_EXTENSIONS:
        return True
    else:
        return False
