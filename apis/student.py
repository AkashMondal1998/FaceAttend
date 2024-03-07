from core.student import Student
from flask_restx import Resource, Namespace, fields
import base64

api = Namespace("student", description="Student related operations")


add = api.model(
    "Add",
    {
        "name": fields.String(required=True, desciption="Name of the student"),
        "email": fields.String(required=True, desciption="Email of the student"),
        "image": fields.String(
            required=True, desciption="Base64 string  of the student's image file"
        ),
    },
)


# Add student info to the database and also accept an image of the student
# expect base64 encoded string from the client
# Need to convert the base64 string to byte object for database storage
@api.route("/add")
class add(Resource):
    @api.expect(add)
    def post(self):
        # call the Face.add_face function to the add the face to the database
        image = api.payload["image"]
        # convert the base64 encoded string to byte object
        image = base64.b64decode(image)
        Student.add(api.payload["name"], api.payload["email"], image)
