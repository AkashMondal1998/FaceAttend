from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from flask_apscheduler import APScheduler
from flask_mail import Mail


class Base(DeclarativeBase, MappedAsDataclass):
    pass


db = SQLAlchemy(model_class=Base)
flask_bcrypt = Bcrypt()
scheduler = APScheduler()
mail = Mail()
