from datetime import datetime
from sqlalchemy import Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class UserMoviesWatchlist(db.Model):
    __tablename__ = "user_movies_watchlist"
    __table_args__ = (
        db.Index("idx_user_movies_watchlist_pagination", "user_id", "updated_at", "api_movie_id"),
    )

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    api_movie_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class UserSeriesWatchlist(db.Model):
    __tablename__ = "user_series_watchlist"
    __table_args__ = (
        db.Index("idx_user_series_watchlist_pagination", "user_id", "updated_at", "api_serie_id"),
    )

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    api_serie_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
