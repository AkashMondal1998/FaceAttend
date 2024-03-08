from face_recognition import face_locations, face_encodings, load_image_file
from .extensions import mysql
from .utils import generate_std_id, send_email, give_file_ext, give_dict
import os


UPLOAD_FOLDER = "photos"


class Student:
    # Add the name ,std_id email,face encoding bytes to the database for the specific student
    @staticmethod
    def add(name, email, img_file):
        cur = mysql.connection.cursor()
        # check if the student is already present in the database using email as it should be unique for every student
        cur.execute("SELECT * FROM students WHERE email = %s", (email,))
        if cur.rowcount != 0:
            return False
        # generate the student_id
        std_id = generate_std_id()
        img_file = std_id + give_file_ext(img_file)
        cur.execute(
            "INSERT INTO students (name,email,std_id,std_img) VALUES(%s,%s,%s,%s)",
            (name, email, std_id, img_file),
        )
        mysql.connection.commit()
        send_email(name, std_id, email)
        return img_file

    # Delete the student from database given its std_id
    @staticmethod
    def delete(std_id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT std_img FROM students WHERE std_id = %s", (std_id,))
        std_img = cur.fetchone()
        if not std_img:
            return False
        cur.execute("DELETE FROM students WHERE std_id = %s", (std_id,))
        mysql.connection.commit()

        # remove the associated student image from the filesystem
        os.remove(os.path.join(UPLOAD_FOLDER, std_img[0]))
        return True

    # read all the face_encodings and names from the database and return and list containg all the known face_encodings and name
    @staticmethod
    def load():
        cur = mysql.connection.cursor()
        cur.execute("SELECT name,std_img FROM students")
        results = cur.fetchall()
        known_std_names = [result[0] for result in results]
        known_std_imgs = [result[1] for result in results]
        known_std_encodings = list()
        for img in known_std_imgs:
            img = load_image_file(os.path.join(UPLOAD_FOLDER, img))
            faceloc = face_locations(img)
            face_encode = face_encodings(img, faceloc, 1)[0]
            known_std_encodings.append(face_encode)
        return known_std_names, known_std_encodings

    # return all the student details from the database as a dictionary
    @staticmethod
    def student_list():
        cur = mysql.connection.cursor()
        cur.execute("SELECT name,email,std_id,std_img FROM students")
        students = cur.fetchall()
        std_list = [give_dict(student) for student in students]
        return std_list

    # return details for a single student give their student id
    @staticmethod
    def student(std_id):
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT name,email,std_id,std_img FROM students WHERE std_id = %s",
            (std_id,),
        )
        student = cur.fetchone()
        std_dict = give_dict(student)
        return std_dict
