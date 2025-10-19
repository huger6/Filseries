from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin
from app.extensions import db, bcrypt

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    pass_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    @classmethod
    def create_user(cls, email, username, password):
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = cls(username=username, email=email, pass_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
    

