from flask import Flask
from core.extensions import mysql
from apis import api
import os

UPLOAD_FOLDER = "photos"

app = Flask(__name__, static_folder=UPLOAD_FOLDER)


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MYSQL_USER"] = os.environ["db_user"]
app.config["MYSQL_PASSWORD"] = os.environ["db_pass"]
app.config["MYSQL_DB"] = "project"

api.init_app(app)
mysql.init_app(app)


if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, port=8080)
