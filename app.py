from flask import Flask
from config import Config
import os


config = Config()

app = Flask(__name__, static_folder=config.UPLOAD_FOLDER)

app.config.from_object(config)

app, scheduler, db = config.init_app(app)


if __name__ == "__main__":
    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    scheduler.start()
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=8080)
