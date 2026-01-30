from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class UserMoviesWatchlist(db.Model):
    __tablename__ = "user_movies_watchlist"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    api_movie_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    updated_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)


class UserSeriesWatchlist(db.Model):
    __tablename__ = "user_series_watchlist"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    api_serie_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    updated_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
