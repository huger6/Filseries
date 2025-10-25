from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db

class UserMoviesWatchlist(db.Model):
    __tablename__ = "user_movies_watchlist"

    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    movie_id : Mapped[int] = mapped_column(Integer, primary_key=True)


class UserSeriesWatchlist(db.Model):
    __tablename__ = "user_series_watchlist"

    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    serie_id : Mapped[int] = mapped_column(Integer, primary_key=True)


# If using titles tables, add:
# ForeignKey("series.serie_id", ondelete="CASCADE")
