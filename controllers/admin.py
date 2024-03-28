from flask_restx import Namespace, Resource
from flask import abort, session
from models.admin import Admin
from forms.admin import AdminLoginForm
from extensions import flask_bcrypt
from .helpers import login_required

api = Namespace("admin", description="Admin related operations")


@api.route("/login")
class Login(Resource):
    def post(self):
        """Admin Login"""

        form = AdminLoginForm()
        if form.validate_on_submit():
            username, password = form.username.data, form.password.data
            admin = Admin.load(username)
            if not admin:
                abort(400, "Wrong Username!")
            if not flask_bcrypt.check_password_hash(admin.password, password):
                abort(400, "Wrong Password!")

            session["username"] = username
            session["role"] = admin.role
            session.permanent = True
            return {"message": "Logged In successfully"}
        return form.errors, 400


@api.route("/logout")
class Logout(Resource):
    @login_required("admin")
    def post(self):
        """Admin Logout"""

        session.clear()
        return {"message": "Logged Out successfully"}
