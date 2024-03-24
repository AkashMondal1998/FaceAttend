from extensions import db, flask_bcrypt
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(60))
    role: Mapped[str] = mapped_column(String(4), default="user", init=False)

    def add(self):
        """Add an user"""

        self.password = flask_bcrypt.generate_password_hash(self.password)
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete an user"""

        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def load(email):
        """Load an user given their email"""

        return db.session.scalars(
            db.select(User).where(User.email == email)
        ).one_or_none()

    @staticmethod
    def user_list():
        """Returns all the users"""

        return db.session.scalars(db.select(User)).all()
