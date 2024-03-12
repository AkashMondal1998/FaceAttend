from face_recognition import face_locations, face_encodings, load_image_file
from .extensions import mysql
from .utils import generate_std_id, send_email, give_file_ext
import os, csv
import MySQLdb.cursors


UPLOAD_FOLDER = "photos"


class Student:

    @staticmethod
    def add(name, email, img_file):
        """Add the name ,std_id email,image file name to the database for the specific student"""

        cur = mysql.connection.cursor()

        # check if the student is already present in the database using email as it should be unique for every student
        cur.execute("SELECT * FROM students WHERE email = %s", (email,))
        if cur.rowcount != 0:
            return False

        # generate the student_id
        std_id = generate_std_id()

        # rename the student image file
        img_file = std_id + give_file_ext(img_file)
        cur.execute(
            "INSERT INTO students (name,email,std_id,std_img) VALUES(%s,%s,%s,%s)",
            (name, email, std_id, img_file),
        )
        mysql.connection.commit()
        send_email(name, std_id, email)
        return img_file

    @staticmethod
    def delete(std_id):
        """Delete the student from database given its std_id"""

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

    @staticmethod
    def load():
        """Read all the image file names and the student names from the database and return and list containg all the known face_encodings and name"""

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

    @staticmethod
    def student_list():
        """Return all the student details from the database"""

        cur = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cur.execute("SELECT name,email,std_id,std_img FROM students")
        students = cur.fetchall()
        return list(students)

    @staticmethod
    def student(std_id):
        """Return details for a single student give their student id from the database"""

        cur = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cur.execute(
            "SELECT name,email,std_id,std_img FROM students WHERE std_id = %s",
            (std_id,),
        )
        student = cur.fetchone()
        return student

    @staticmethod
    def student_csv():
        """Generate csv containing all the students"""

        cur = mysql.connection.cursor()
        cur.execute("SELECT id,name,email,std_id FROM students")
        students = cur.fetchall()
        with open(f"StudentList.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["No", "Name", "Email", "Student_id"])
            writer.writerows(students)
