from .extensions import db, flask_bcrypt
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(60))

    def add(self):
        """Add an user"""

        self.password = flask_bcrypt.generate_password_hash(self.password)
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def load(email):
        """Load an user given their email"""

        return db.session.scalars(
            db.select(User).where(User.email == email)
        ).one_or_none()

    @staticmethod
    def check_user(email, password):
        """Check email and password of the user"""

        user = User.load(email)
        if not user:
            return False
        if not flask_bcrypt.check_password_hash(user.password, password):
            return False
        return True
