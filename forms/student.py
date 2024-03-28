from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileAllowed, FileField, FileSize, FileRequired


class StudentForm(FlaskForm):
    """Student Form"""

    name = StringField("name", validators=[DataRequired(), Length(max=50, min=1)])
    email = StringField(
        "email", validators=[Email(check_deliverability=True), DataRequired()]
    )
    image = FileField(
        "image",
        validators=[
            FileRequired(),
            FileAllowed(
                ["jpg", "jpeg", "png"], message="File extension not supported!"
            ),
            FileSize(
                max_size=1000000, message="File size must less than or equal to 1mb"
            ),
        ],
    )
