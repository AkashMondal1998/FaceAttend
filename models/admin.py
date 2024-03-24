from extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Admin(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    username: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(String(60))
    role: Mapped[str] = mapped_column(String(5), default="admin", init=False)

    def add(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def load(username):
        return db.session.scalars(
            db.select(Admin).where(Admin.username == username)
        ).one_or_none()
