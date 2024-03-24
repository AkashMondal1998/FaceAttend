import random
from extensions import mail, flask_bcrypt
from flask_mail import Message
from .admin import Admin


def generate_std_id():
    """Generate a random 10 digit number for std_id"""

    return str(random.randint(1000000000, 9999999999))


def send_email(name, std_id, email):
    """Send an email to the student"""

    msg = Message()
    msg.subject = "Successfully Registered!"
    msg.recipients = [email]
    msg.body = f"Hello {name},\n\nWe're delighted to inform you that you have been successfully registered in our system.\n\nYour Student ID is: {std_id}.\n\nThank you for joining us!\n\nBest regards,\nThe Team"

    msg.html = f"""
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
    mail.send(msg)


def give_file_ext(filename):
    """Return the file extension"""

    file_ext = "." + filename.rsplit(".", 1)[1]
    return file_ext


def create_admin():
    """Create the admin account"""

    if not Admin.load("admin"):
        admin = Admin("admin", flask_bcrypt.generate_password_hash("admin"))
        Admin.add(admin)
