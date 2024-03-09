from core.student import Student
from core.utils import allowed_files
from flask import abort, request
from flask_restx import Resource, Namespace, fields
from werkzeug.utils import secure_filename
import os


api = Namespace("students", description="Student related operations")

UPLOAD_FOLDER = "photos"


class ImagePath(fields.Raw):
    def format(self, value):
        return os.path.join(request.url_root, UPLOAD_FOLDER, value)


student_model = api.model(
    "Student_list",
    {
        "name": fields.String,
        "email": fields.String,
        "std_id": fields.String,
        "std_img": ImagePath,
    },
)


# Add student info to the database and also accept an image file of the student
# save the file to the file system
# Expect form data containg name,email,and an image file from the client
@api.route("/add")
class add_student(Resource):
    def post(self):
        if "image" not in request.files:
            return {"msg": "Image file is required"}
        image = request.files["image"]
        name = request.form.get("name")
        email = request.form.get("email")

        # check if the file is of supported format
        if not allowed_files(image.filename):
            abort(400, "Image file extension not supported!")

        filename = secure_filename(image.filename)
        # call the Student.add function to the add the student to the database
        s = Student.add(name, email, filename)
        if not s:
            abort(400, f"Student with email {email} is already present!")

        # save the file to the file system
        image.save(os.path.join(UPLOAD_FOLDER, s))
        return {"msg": f"Student added successfully"}, 201


# Get the details of all the students
@api.route("/get")
class student_list(Resource):
    @api.marshal_list_with(student_model)
    def get(self):
        if not Student.student_list():
            abort(404, "No students presesnt!")
        return Student.student_list()


# Delete a student from the database
@api.route("/delete/<id>")
class delete_student(Resource):
    def delete(self, id):
        if not Student.delete(id):
            abort(404, f"No student with id {id} found!")
        return {"msg": "Student successfully removed!"}


# Get the detail of a single student given their student id
@api.route("/get/<id>")
class student(Resource):
    @api.marshal_with(student_model)
    def get(self, id):
        if not Student.student(id):
            abort(404, f"No student with id {id} found!")
        return Student.student(id)
