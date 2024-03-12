from flask import Flask
from models.extensions import mysql, jwt
from controllers import api
import os
from datetime import timedelta

UPLOAD_FOLDER = "photos"

app = Flask(__name__, static_folder=UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 1 * 1000 * 1000
app.config["MYSQL_USER"] = os.environ["db_user"]
app.config["MYSQL_PASSWORD"] = os.environ["db_pass"]
app.config["MYSQL_DB"] = "project"
app.config["SECRET_KEY"] = "unssesfasf"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)

api.init_app(app)
mysql.init_app(app)


if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, port=8080)
