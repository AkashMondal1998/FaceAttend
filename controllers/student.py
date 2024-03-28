from flask import abort, after_this_request, send_file
from flask_restx import Namespace, Resource, fields
from werkzeug.utils import secure_filename
from controllers.helpers import login_required
from models.student import Student
from forms.student import StudentForm
from .utils import ImageUrl
import os

api = Namespace("students", description="Student related operations")


# student list api response model
student_list_model = api.model(
    "Student_list",
    {
        "name": fields.String(description="Name of the student"),
        "email": fields.String(description="Email of the student"),
        "std_id": fields.String(description="Student id of the student"),
    },
)

# student api response model
student_model = api.model(
    "Student",
    {
        "name": fields.String(description="Name of the student"),
        "email": fields.String(description="Email of the student"),
        "std_id": fields.String(description="Student id of the student"),
        "std_img": ImageUrl(description="Url for the image of the student"),
    },
)


@api.route("/add")
class AddStudent(Resource):
    @login_required("user")
    def post(self):
        """Add a student"""

        form = StudentForm()
        if form.validate_on_submit():
            name, email, image = form.name.data, form.email.data, form.image.data
            filename = secure_filename(image.filename)

            # check if the student is already present in the database
            if Student.load_email(email):
                abort(409, f"Student with email {email} is already present!")

            student = Student(name, email, filename)

            # add the student to the database
            img_file_name = student.add()

            # save the file to the file system
            image.save(os.path.join("photos", img_file_name))
            return {"message": "Student added successfully"}, 201
        return form.errors, 400


@api.route("/get")
class GetAllStudents(Resource):
    @api.marshal_list_with(student_list_model)
    @login_required("user")
    def get(self):
        """Get details of all the students"""

        students = Student.student_list()
        if not students:
            return " ", 204
        return students


@api.route("/get/<std_id>")
class GetStudent(Resource):
    @api.marshal_with(student_model)
    @login_required("user")
    def get(self, std_id):
        """Get details of a single student given their student id"""

        student = Student.student(std_id)
        if not student:
            abort(404, f"Student with id {std_id} not found!")
        return student


@api.route("/delete/<std_id>")
class DeleteStudent(Resource):
    @login_required("user")
    def delete(self, std_id):
        """Delete a student"""

        student = Student.load_std_id(std_id)
        if not student:
            abort(404, f"Student with id {std_id} not found!")

        student.delete()
        return {"message": "Student successfully removed!"}, 200


@api.route("/csv")
class StudentCsv(Resource):
    @login_required("user")
    def get(self):
        """Generate a csv file containing all the student details"""

        # check if students are present
        if not Student.student_list():
            return " ", 204

        @after_this_request
        def delete_file(response):
            os.remove("StudentList.csv")
            return response

        Student.student_csv()
        return send_file("StudentList.csv", as_attachment=True)
