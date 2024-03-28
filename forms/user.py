from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class UserForm(FlaskForm):
    """User Form"""

    name = StringField("name", validators=[DataRequired(), Length(max=50, min=1)])
    email = StringField(
        "email", validators=[Email(check_deliverability=True), DataRequired()]
    )
    password = PasswordField("password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "confirm_password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Confirm password has to be same as password",
            ),
        ],
    )


class UserLoginForm(FlaskForm):
    """User Login Form"""

    email = StringField(
        "email", validators=[Email(check_deliverability=True), DataRequired()]
    )
    password = PasswordField("password", validators=[DataRequired()])
