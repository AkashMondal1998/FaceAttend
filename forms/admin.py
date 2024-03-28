from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class AdminLoginForm(FlaskForm):
    """Admin Login Form"""

    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
