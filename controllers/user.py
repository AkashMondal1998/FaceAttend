from flask import abort, request, session
from flask_restx import Namespace, Resource, fields
from controllers.helpers import login_required
from models.user import User
from .utils import check_email
from extensions import flask_bcrypt

api = Namespace("user", description="User related operations")


user = api.model(
    "user info",
    {
        "name": fields.String(description="Name of the user"),
        "email": fields.String(description="Email of the user"),
    },
)

user_list = api.model(
    "user_list",
    {
        "name": fields.String(description="User's Name"),
        "email": fields.String(description="User's Email"),
    },
)


@api.route("/login")
class login(Resource):
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

        # load the user
        user = User.load(email)

        # check the user details
        if not user:
            abort(400, "Wrong email!")
        if not flask_bcrypt.check_password_hash(user.password, password):
            abort(400, "Wrong password!")

        session["email"] = user.email
        session["name"] = user.name
        session["role"] = user.role
        session.permanent = True
        return {"message": "Logged In successfully"}


@api.route("/logout")
class Logout(Resource):
    @login_required("user")
    def post(self):
        """Logout User"""

        session.clear()
        return {"message": "Logged Out successfully"}


@api.route("/add")
class Add(Resource):
    @login_required("admin")
    def post(self):
        """Add User"""

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

        # check if the user is already added
        if User.load(email):
            abort(409, "User is already added!")

        user = User(name, email, password)

        # add the user
        user.add()

        return {"message": "Successfully added!"}, 201


@api.route("/delete/<email>")
class Delete(Resource):
    @login_required("admin")
    def delete(self, email):
        """Delete an user"""

        user = User.load(email)
        if not user:
            abort(400, f"No user with email {email}!")
        user.delete()
        return {"message": "User deleted!"}


@api.route("/info")
class UserInfo(Resource):
    @api.marshal_with(user)
    @login_required("user")
    def get(self):
        """Get the authenticated user info"""

        return session


@api.route("/get")
class UserList(Resource):
    @api.marshal_list_with(user_list)
    @login_required("admin")
    def get(self):
        "User List"

        users = User.user_list()
        if not users:
            return " ", 204
        return users
