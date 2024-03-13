from flask_restx import Resource, Namespace
from flask import jsonify, session, request, abort


api = Namespace("admin", description="Admin related operations")


@api.route("/login")
class login(Resource):
    def post(self):
        """Login User"""

        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            abort(400, "Username is required")
        if not password:
            abort(400, "Password is required")

        # check if the user is already logged in
        if "username" in session:
            abort(400, "You are already logged in!")

        # If user has checked the remember me checkbox
        # Then set the cookie expirtion time to 7 days
        if request.form.get("remember"):
            session.permanent = True

        session["username"] = request.form.get("username")
        return {"message": "Logged In successfully"}


@api.route("/logout")
class Logout(Resource):

    def post(self):
        """Logout User"""

        # check if the user is logged in
        if "username" not in session:
            abort(401, "Please log in first before attempting to log out.")

        session.clear()
        return {"message": "Logged Out successfully"}
