import os
import secrets
from datetime import timedelta
from sqlalchemy import URL
from flask_session import Session
from extensions import flask_bcrypt, db, scheduler, mail
from controllers import api

url = URL.create(
    "mysql",
    username=os.environ["db_user"],
    password=os.environ["db_pass"],
    host=os.environ["db_host"],
    database="project",
)


class Config:
    UPLOAD_FOLDER = "photos"
    MAX_CONTENT_LENGTH = 1 * 1000 * 1000
    SQLALCHEMY_DATABASE_URI = url
    SECRET_KEY = secrets.token_hex(16)
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_TYPE = "sqlalchemy"
    SESSION_SQLALCHEMY = db
    SESSION_COOKIE_SAMESITE = "Strict"
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ["mail_user"]
    MAIL_PASSWORD = os.environ["mail_password"]
    MAIL_DEFAULT_SENDER = os.environ["mail_user"]
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_SUPPRESS_SEND = True

    @staticmethod
    def init_app(app):
        api.init_app(app)
        flask_bcrypt.init_app(app)
        db.init_app(app)
        Session(app)
        scheduler.init_app(app)
        mail.init_app(app)

        return app, scheduler, db
