from flask import Flask
from config import Config
from models.utils import create_admin
import os


config = Config()

app = Flask(__name__, static_folder=config.UPLOAD_FOLDER)

app.config.from_object(config)

app, db = config.init_app(app)


if __name__ == "__main__":
    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    with app.app_context():
        db.create_all()
        create_admin()
    app.run(debug=True, host="0.0.0.0", port=8080)
