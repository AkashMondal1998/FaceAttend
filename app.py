from flask import Flask
from sqlalchemy import URL
from flask_session import Session
from models.extensions import flask_bcrypt, db
from controllers import api
import os
from datetime import timedelta
import secrets

UPLOAD_FOLDER = "photos"

app = Flask(__name__, static_folder=UPLOAD_FOLDER)

url = URL.create(
    "mysql",
    username=os.environ["db_user"],
    password=os.environ["db_pass"],
    host="localhost",
    database="project",
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 1 * 1000 * 1000
app.config["SQLALCHEMY_DATABASE_URI"] = url
app.config["SECRET_KEY"] = secrets.token_hex(16)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = ".session"
app.config["SESSION_PERMANENT"] = False

api.init_app(app)
flask_bcrypt.init_app(app)
db.init_app(app)
Session(app)

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=8080)
