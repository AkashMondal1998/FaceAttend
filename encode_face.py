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
    # add the face encoding bytes to the database for the specific person
    @staticmethod
    def add_face(name, img_file):
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
            return "Face Added!"
        except sqlite3.IntegrityError:
            return "Face already exists!"

    # read all the face_encodings and names from the database and return and list containg all the known face_encodings and name
    @staticmethod
    def load_faces():
        con = connect()
        cur = con.cursor()
        cur.execute("SELECT name,face_encoding FROM persons")
        encodings = cur.fetchall()
        known_face_encodings = [encoding[1] for encoding in encodings]
        known_face_names = [name[0] for name in encodings]
        known_face_encodings = [
            np.frombuffer(encoding, dtype="float64")
            for encoding in known_face_encodings
        ]
        con.close()
        return known_face_encodings, known_face_names
