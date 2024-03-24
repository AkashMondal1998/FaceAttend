from flask_restx import Namespace, Resource
from flask import request, abort, session
from models.admin import Admin
from extensions import flask_bcrypt
from .helpers import login_required

api = Namespace("admin", description="Admin related operations")


@api.route("/login")
class Login(Resource):
    def post(self):
        """Admin Login"""

        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            abort(400, "Username is required!")
        if not password:
            abort(400, "Password is required!")

        admin = Admin.load(username)
        if not admin:
            abort(400, "Wrong Username!")
        if not flask_bcrypt.check_password_hash(admin.password, password):
            abort(400, "Wrong Password!")

        session["username"] = username
        session["role"] = admin.role
        session.permanent = True
        return {"message": "Logged In successfully"}


@api.route("/logout")
class Logout(Resource):
    @login_required("admin")
    def post(self):
        """Admin Logout"""

        session.clear()
        return {"message": "Logged Out successfully"}
