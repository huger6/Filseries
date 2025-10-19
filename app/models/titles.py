from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db

class Movies(db.Model):
    __tablename__ = "movies"

    movie_id : Mapped[int] = mapped_column(Integer, primary_key=True)
    movie_tconst = Column(String(15), unique=True, index=False)


class Series(db.Model):
    __tablename__ = "series"

    serie_id : Mapped[int] = mapped_column(Integer, primary_key=True)
    serie_tconst = Column(String(15), unique=True, index=False)

