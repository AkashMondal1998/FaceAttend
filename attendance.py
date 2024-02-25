import sqlite3
import csv
from datetime import datetime, date


def connect():
    """Returns a connection object"""
    return sqlite3.connect("valid_persons.db")


class Attendance:
    # Returns True if already marked and False if not marked
    @staticmethod
    def if_marked(face_encoding):
        con = connect()
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM attendance WHERE date = ? AND user_id = (SELECT id FROM persons WHERE face_encoding = ?)",
            (datetime.today().strftime("%d-%m-%Y"), face_encoding.tobytes()),
        )
        if not cur.fetchone():
            return False
        else:
            return True

    # mark attendance of a detected person
    @staticmethod
    def mark_attendance(face_encodings: list):
        con = connect()
        cur = con.cursor()
        for encoding in face_encodings:
            if not Attendance.if_marked(encoding):
                cur.execute(
                    "SELECT id from persons WHERE face_encoding = ?",
                    (encoding.tobytes()),
                )
                user_id = cur.fetchone()[0]
                cur.execute(
                    "INSERT INTO attendance(date,user_id) VALUES(?,?)",
                    (datetime.today().strftime("%d-%m-%Y"), user_id),
                )

    # generate a csv with the attendance for a particular date
    @staticmethod
    def generate_csv(date_for_attendance):
        try:
            date.fromisoformat(date_for_attendance)
        except ValueError:
            return "Wrong date format!"
        con = connect()
        cur = con.cursor()
        cur.execute(
            "SELECT name,emp_id FROM persons WHERE id = (SELECT user_id FROM attendance WHERE date = ?)",
            (date_for_attendance),
        )
        results = cur.fetchall()
        if not results:
            return f"No data available for {date_for_attendance}"
        with open(f"{date_for_attendance}.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Emp_id"])
            for result in results:
                writer.writerow(result)
        return f"CSV file generated!"
