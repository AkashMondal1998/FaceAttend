from flask_restx import Resource, Namespace


api = Namespace("admin", description="Admin related operations")


# Get username and password then validate
@api.route("/login")
class login(Resource):
    def post():
        pass
