from core.student import Student
from core.utils import allowed_files, ImageUrl
from flask import abort, request
from flask_restx import Resource, Namespace, fields
from werkzeug.utils import secure_filename
import os

api = Namespace("students", description="Student related operations")


UPLOAD_FOLDER = "photos"

student_model = api.model(
    "Student_list",
    {
        "name": fields.String(description="Name of the student"),
        "email": fields.String(description="Email of the student"),
        "std_id": fields.String(description="Student id of the student"),
        "std_img": ImageUrl(description="Url for the image of the student"),
    },
)


@api.route("/add")
class add_student(Resource):
    """
    Add student info to the database and also accept an image file of the student
    save the file to the file system
    Expect form data containg name,email,and an image file from the client
    """

    def post(self):
        if "image" not in request.files:
            abort(400, "Image is required!")
        image = request.files["image"]
        if not image:
            abort(400, "Image is requried!")
        name = request.form.get("name")
        if not name:
            abort(400, "Name cannnot be blank!")
        email = request.form.get("email")
        if not email:
            abort(400, "Email cannot be blank")

        # check if the file is of supported format
        if not allowed_files(image.filename):
            abort(400, "Image file extension not supported!")

        filename = secure_filename(image.filename)
        # call the Student.add function to the add the student to the database
        s = Student.add(name, email, filename)
        if not s:
            abort(409, f"Student with email {email} is already present!")

        # save the file to the file system
        image.save(os.path.join(UPLOAD_FOLDER, s))
        return {"message": f"Student added successfully"}, 201


@api.route("/get")
class student_list(Resource):
    """Return the details of all the students"""

    @api.marshal_list_with(student_model)
    def get(self):
        if not Student.student_list():
            abort(404, "No students are present!")
        return Student.student_list()


@api.route("/delete/<std_id>")
class delete_student(Resource):
    """Delete a student from the database"""

    def delete(self, std_id):
        if not Student.delete(std_id):
            abort(404, f"Student with id {std_id} not found!")
        return {"message": "Student successfully removed!"}


@api.route("/get/<std_id>")
class student(Resource):
    """Returns the detail of a single student given their student id"""

    @api.marshal_with(student_model)
    def get(self, std_id):
        if not Student.student(std_id):
            abort(404, f"Student with id {std_id} not found!")
        return Student.student(std_id)
