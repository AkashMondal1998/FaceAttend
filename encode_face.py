from face_recognition import (
    face_encodings,
    load_image_file,
    face_locations,
)
import sqlite3
import numpy as np


def connect():
    """Returns a connection object"""
    return sqlite3.connect("valid_persons.db")


class Face:
    def add_face(self, img_file, name):
        """Todo: add the face encoding bytes to the database for the specific person"""
        img = load_image_file(img_file)
        faceloc = face_locations(img)
        face_encode = face_encodings(img, faceloc, 1)[0]
        con = connect()
        cur = con.cursor()
        try:
            cur.execute(
                "INSERT INTO persons (name,face_encoding) VALUES(?,?)",
                (name, face_encode.tobytes()),
            )
            con.commit()
            con.close()
            return "Person Added"
        except sqlite3.IntegrityError:
            return "Person already exists!"

    def load_faces(self):
        """Todo: read all the face_encodings from the database and return and list
        Containg all the known face_encodings"""
        con = connect()
        cur = con.cursor()
        cur.execute("SELECT face_encoding FROM persons")
        encodings = cur.fetchall()
        known_face_encodings = [encoding[0] for encoding in encodings]

        known_face_encodings = [
            np.frombuffer(encoding, dtype="float64")
            for encoding in known_face_encodings
        ]
        con.close()
        return known_face_encodings
