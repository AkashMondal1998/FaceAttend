from .utils import generate_std_id, send_email
import numpy as np
from face_recognition import face_locations, face_encodings


class Student:
    # Add the name ,std_id email,face encoding bytes to the database for the specific student
    @staticmethod
    def add(name, email, img_file):

        # convert the base64 encoded string to numpy array
        img = np.frombuffer(img_file, dtype="uint8")
        faceloc = face_locations(img)
        face_encoding = face_encodings(img, faceloc, 1)[0]

        # generate the student_id
        std_id = generate_std_id()
        cur.execute(
            "INSERT INTO persons (name,email,emp_id,face_encoding) VALUES(?,?,?,?)",
            (name, email, std_id, face_encoding.tobytes()),
        )
        con.commit()
        con.close()
        send_email(name, std_id, email.normalized)
        return f"Face added for {name} with employee id {std_id}"
