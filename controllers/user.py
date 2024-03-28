from flask import abort, session
from flask_restx import Namespace, Resource, fields
from controllers.helpers import login_required
from models.user import User
from forms.user import UserForm, UserLoginForm
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

        form = UserLoginForm()
        if form.validate_on_submit():
            email, password = form.email.data, form.password.data

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
        return form.errors, 400


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

        form = UserForm()
        if form.validate_on_submit():
            name, email, password = form.name.data, form.email.data, form.password.data

            # check if the user is already added
            if User.load(email):
                abort(409, "User is already added!")

            user = User(name, email, password)

            # add the user
            user.add()

            return {"message": "Successfully added!"}, 201
        return form.errors, 400


@api.route("/delete/<email>")
class Delete(Resource):
    @login_required("admin")
    def delete(self, email):
        """Delete an user"""

        user = User.load(email)
        if not user:
            abort(404, f"No user with email {email}")
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
