import random
from email.message import EmailMessage
import smtplib
import os

UPLOAD_FOLDER = "photos"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


# generate a random 10 digit number for std_id
def generate_std_id():
    return str(random.randint(1000000000, 9999999999))


# Send an email to the student
def send_email(name, std_id, email):
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        msg = EmailMessage()
        msg.set_content(
            f"Hello {name},\n\nWe're delighted to inform you that you have been successfully registered in our system.\n\nYour Student ID is: {std_id}.\n\nThank you for joining us!\n\nBest regards,\nThe Team"
        )
        msg["Subject"] = "Successfully Registered!"
        msg["From"] = os.environ["mail_user"]
        msg["To"] = email
        smtp.login(os.environ["mail_user"], os.environ["mail_password"])
        smtp.send_message(msg)


# check the extension of file that is being saved
def allowed_files(filename):
    filename = filename.strip()
    file_ext = filename.rsplit(".", 1)[1]
    if file_ext in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


# return the file extension
def give_file_ext(filename):
    file_ext = "." + filename.rsplit(".", 1)[1]
    return file_ext


# return a response dict
def give_dict(std_list):
    std_dict = dict()
    (
        std_dict["name"],
        std_dict["email"],
        std_dict["std_id"],
        std_dict["std_img"],
    ) = (
        std_list[0],
        std_list[1],
        std_list[2],
        os.path.join(UPLOAD_FOLDER, std_list[3]),
    )
    return std_dict
