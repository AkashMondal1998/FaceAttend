from flask import abort, request, session
from flask_restx import Namespace, Resource

from models.helpers import is_logged_in, login_required
from models.user import User
from models.utils import check_email

api = Namespace("admin", description="Admin related operations")


@api.route("/login")
class login(Resource):

    @is_logged_in
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

        user = User(email, password)

        # check if the email and password are valid
        if not user.check_user():
            abort(400, "Email or password is wrong!")

        # if user has checked the remember me checkbox
        # then set the cookie expiration time to 7 days
        if request.form.get("remember"):
            session.permanent = True

        session["email"] = request.form.get("email")
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

    @is_logged_in
    def post(self):
        """Register User"""

        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # check if the any of the given fields are blank
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

        user = User(email, password)

        # check if the user is already registered
        if not user.add_user():
            abort(400, "You are already registered!")

        return {"message": "Successfully registered!"}
