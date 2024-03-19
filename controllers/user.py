from flask import abort, request, session
from flask_restx import Namespace, Resource, fields
from controllers.helpers import if_logged_in, login_required
from models.user import User
from .utils import check_email

api = Namespace("user", description="User related operations")


user = api.model(
    "user info",
    {
        "name": fields.String(description="Name of the user"),
        "email": fields.String(description="Email of the user"),
    },
)


@api.route("/login")
class login(Resource):
    @if_logged_in
    def post(self):
        """Login User"""

        email = request.form.get("email")
        password = request.form.get("password")

        # check if the any of the given fields are blank
        if not email:
            abort(400, "Email is required")
        if not password:
            abort(400, "Password is required")

        # check if email is valid
        email, ret = check_email(email)
        if not ret:
            abort(400, email)

        # check if the email and password are valid
        if not User.check_user(email, password):
            abort(400, "Email or password is wrong!")

        # load the user to get the user's name
        name = User.load(email).name

        session["email"] = request.form.get("email")
        session["name"] = name
        return {"message": "Logged In successfully"}


@api.route("/logout")
class Logout(Resource):
    @login_required
    def post(self):
        """Logout User"""

        session.clear()
        return {"message": "Logged Out successfully"}


@api.route("/register")
class Register(Resource):
    @if_logged_in
    def post(self):
        """Register User"""

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # check if the any of the given fields are blank
        if not name:
            abort(400, "Name is required!")
        if not email:
            abort(400, "Email is required!")
        if not password:
            abort(400, "Password is required")
        if not confirm_password:
            abort(400, "Confirm Password is required")

        if password != confirm_password:
            abort(400, "Password and confirm password has to be same!")

        # check if email is a valid email address
        email, ret = check_email(email)
        if not ret:
            abort(400, email)

        # check if the user is already registered
        if User.load(email):
            abort(403, "You are already registered!")

        user = User(name, email, password)

        # add the user
        user.add()

        return {"message": "Successfully registered!"}, 201


@api.route("/get")
class UserInfo(Resource):
    @api.marshal_with(user)
    @login_required
    def get(self):
        """Get the authenticated  user info"""

        return session
