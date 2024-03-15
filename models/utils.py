import os
import random
import smtplib
from email.message import EmailMessage

from email_validator import EmailNotValidError, validate_email
from flask import request
from flask_restx import fields

UPLOAD_FOLDER = "photos"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def generate_std_id():
    """Generate a random 10 digit number for std_id"""
    return str(random.randint(1000000000, 9999999999))


def send_email(name, std_id, email):
    """Send an email to the student"""

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        msg = EmailMessage()
        msg.set_content(
            f"Hello {name},\n\nWe're delighted to inform you that you have been successfully registered in our system.\n\nYour Student ID is: {std_id}.\n\nThank you for joining us!\n\nBest regards,\nThe Team"
        )
        html_content = f"""
        <html>
        <head>
            <style>
                /* Add CSS styling here */
                body {{
                    font-family: Arial, sans-serif;
                    font-size: 14px;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    margin: 20px auto;
                    max-width: 600px;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    background-color: #e4c9ab;
                    color: #fff;
                    padding: 10px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    padding: 20px;
                }}
                .student-info {{
                    background-color: #f0f0f0;
                    padding: 10px;
                    border-radius: 5px;
                    margin-bottom: 10px;
                }}
                .student-name {{
                    font-weight: bold;
                    color: #333; /* Neutral dark color */
                }}
                .student-id {{
                    font-style: italic;
                    color: #555; /* Slightly darker neutral color */
                }}
                .footer {{
                    padding-top: 20px;
                    text-align: center;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome</h1>
                </div>
                <div class="content">
                    <div class="student-info">
                        <span class="student-name">Hello {name},</span><br>
                        <span>We're delighted to inform you that you have been successfully registered in our system.</span><br>
                        <span class="student-id">Your Student ID is: {std_id}.</span><br>
                        <span>Thank you for joining us!</span>
                    </div>
                </div>
                <div class="footer">
                    <p>Best regards,<br>The Team</p>
                </div>
            </div>
        </body>
        </html>
        """

        msg.add_alternative(html_content, subtype="html")

        msg["Subject"] = "Successfully Registered!"
        msg["From"] = os.environ["mail_user"]
        msg["To"] = email
        smtp.login(os.environ["mail_user"], os.environ["mail_password"])
        smtp.send_message(msg)


def allowed_files(filename):
    """Check the extension of file that is being saved"""

    filename = filename.strip()
    file_ext = filename.rsplit(".", 1)[1].lower()
    if file_ext in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


def give_file_ext(filename):
    """Return the file extension"""

    file_ext = "." + filename.rsplit(".", 1)[1]
    return file_ext


class ImageUrl(fields.Raw):
    """Custom field for student image for the student_model response"""

    def format(self, value):
        return os.path.join(request.url_root, UPLOAD_FOLDER, value)


def check_email(email):
    """Check if email is valid or not and also checks if the email is deliverable"""

    try:
        email_info = validate_email(email, check_deliverability=True)
    except EmailNotValidError as e:
        return str(e), False
    return email_info.normalized, True
