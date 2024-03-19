from extensions import db
from face_recognition import load_image_file, face_encodings, face_locations
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, select
from .utils import generate_std_id, give_file_ext, send_email
import os
import csv


UPLOAD_FOLDER = "photos"


class Student(db.Model):
    "Student Model"

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255))
    std_id: Mapped[str] = mapped_column(
        String(10), default_factory=generate_std_id, init=False
    )
    std_img: Mapped[str] = mapped_column(String(255))

    def add(self):
        """add a student amd return the student image file name"""

        # rename the student image file
        self.std_img = self.std_id + give_file_ext(self.std_img)

        db.session.add(self)
        db.session.commit()

        # send a conformation email to the student
        send_email(self.name, self.std_id, self.email)

        return self.std_img

    @staticmethod
    def load_email(email):
        """load a student given their email"""

        return db.session.scalars(
            db.select(Student).where(Student.email == email)
        ).one_or_none()

    @staticmethod
    def load_std_id(std_id):
        """load a student given their student id"""

        return db.session.scalars(
            db.select(Student).where(Student.std_id == std_id)
        ).one_or_none()

    @staticmethod
    def delete(std_id):
        """delete a student give their student id"""

        # get the student image file name
        std_img = Student.load_std_id(std_id).std_img

        db.session.execute(db.delete(Student).where(Student.std_id == std_id))
        db.session.commit()

        # remove the associated student image from the filesystem
        os.remove(os.path.join(UPLOAD_FOLDER, std_img))

    @staticmethod
    def student_list():
        "load all the students present"

        return db.session.scalars(db.select(Student)).all()

    @staticmethod
    def student(std_id):
        """load a particular user given their student id"""

        return db.session.scalars(
            db.select(Student).where(Student.std_id == std_id)
        ).one_or_none()

    @staticmethod
    def load():
        """load the student names and student face encodings"""

        with db.engine.connect() as conn:
            results = conn.execute(select(Student.name, Student.std_img)).all()

        known_std_names = [result[0] for result in results]
        known_std_imgs = [result[1] for result in results]
        known_std_encodings = list()
        for img in known_std_imgs:
            img = load_image_file(os.path.join(UPLOAD_FOLDER, img))
            faceloc = face_locations(img)
            face_encode = face_encodings(img, faceloc, 1)[0]
            known_std_encodings.append(face_encode)
        return known_std_names, known_std_encodings

    @staticmethod
    def student_csv():
        """generate a csv file containing all the student details"""

        with db.engine.connect() as conn:
            students = conn.execute(
                select(Student.id, Student.name, Student.email, Student.std_id)
            ).all()

        with open("StudentList.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["No", "Name", "Email", "Student_id"])
            writer.writerows(students)
