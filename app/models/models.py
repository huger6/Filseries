from sqlalchemy import Column, Integer, String
from flask_login import UserMixin
from extensions import db, bcrypt

class User(db.Model, UserMixin): #db.Model represents a table, UserMixin used to say that this is related to users
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique= True, nullable=False, index=True)
    pass_hash = Column(String(255), nullable=False)

    @classmethod
    def create_user(cls, email, username, password):
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = cls(username=username, email=email, pass_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        


