from flask import Flask
from core.extensions import mysql
from apis import api


app = Flask(__name__)

UPLOAD_FOLDER = "photos"


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MYSQL_USER"] = "akash"
app.config["MYSQL_PASSWORD"] = "akash"
app.config["MYSQL_DB"] = "project"

api.init_app(app)
mysql.init_app(app)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
