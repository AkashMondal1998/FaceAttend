from .utils import generate_std_id, send_email
import numpy as np


class Student:
    # Add the name ,std_id email,face encoding bytes to the database for the specific student
    @staticmethod
    def add(name, email, img_file):
        img = np.frombuffer(img_file, dtype="uint8")
        faceloc = face_locations(img)
        face_encode = face_encodings(img, faceloc, 1)[0]
        emp_id = generate_emp_id()
        cur.execute(
            "INSERT INTO persons (name,email,emp_id,face_encoding) VALUES(?,?,?,?)",
            (name, email.normalized, emp_id, face_encode.tobytes()),
        )
        con.commit()
        con.close()
        send_email(name, emp_id, email.normalized)
        return f"Face added for {name} with employee id {emp_id}"
