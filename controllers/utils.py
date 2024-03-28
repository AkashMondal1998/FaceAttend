from flask_restx import fields
from flask import request
import os


class ImageUrl(fields.Raw):
    """Custom field for student image for the student_model response"""

    def format(self, value):
        return os.path.join(request.url_root, "photos", value)
