from sqlalchemy import Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db

class UserMoviesSeen(db.Model):
    __tablename__ = "user_movies_seen"

    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    movie_id : Mapped[int] = mapped_column(Integer, primary_key=True)
    date : Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    obs : Mapped[String | None] = mapped_column(String(255), nullable=True)
    rating : Mapped[Float | None] = mapped_column(Float, nullable=True)

class UserSeriesSeen(db.Model):
    __tablename__ = "user_series_seen"

    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    serie_id : Mapped[int] = mapped_column(Integer, primary_key=True)
    date : Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    obs : Mapped[String | None] = mapped_column(String(255), nullable=True)
    rating : Mapped[Float | None] = mapped_column(Float, nullable=True)

# If using titles tables, add:
# ForeignKey("series.serie_id", ondelete="CASCADE")

