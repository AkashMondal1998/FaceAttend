import random
from email.message import EmailMessage
import smtplib
import os


# generate a random 10 digit number for std_id
def generate_std_id():
    return str(random.randint(1000000000, 9999999999))


# Send an email to the employee
def send_email(name, emp_id, email):
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        msg = EmailMessage()
        msg.set_content(
            f"Hello {name},\n\nWe're delighted to inform you that you have been successfully registered in our system.\n\nYour employee ID is: {emp_id}.\n\nThank you for joining us!\n\nBest regards,\nThe Team"
        )
        msg["Subject"] = "Successfully Registered!"
        msg["From"] = os.environ["mail_user"]
        msg["To"] = email
        smtp.login(os.environ["mail_user"], os.environ["mail_password"])
        smtp.send_message(msg)
