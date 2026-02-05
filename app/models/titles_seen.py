from datetime import datetime
from sqlalchemy import Integer, Float, DateTime, ForeignKey, Enum, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db

# Series progress status types
SERIES_STATUS_TYPES = ("New Season Available", "Seen", "Watching")


class UserMoviesSeen(db.Model):
    __tablename__ = "user_movies_seen"
    __table_args__ = (
        CheckConstraint("user_rating >= 0.0 AND user_rating <= 10.0", name="check_movie_rating_range"),
        db.Index("idx_user_movies_seen_pagination", "user_id", "updated_at", "api_movie_id"),
    )

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    api_movie_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class UserSeriesProgress(db.Model):
    __tablename__ = "user_series_progress"
    __table_args__ = (
        CheckConstraint("user_rating >= 0.0 AND user_rating <= 10.0", name="check_series_rating_range"),
        db.Index("idx_user_series_progress_pagination", "user_id", "updated_at", "api_serie_id"),
    )

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    api_serie_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    last_season_seen: Mapped[int | None] = mapped_column(Integer, default=1, nullable=True)
    status: Mapped[str | None] = mapped_column(Enum(*SERIES_STATUS_TYPES, name="series_status"), nullable=True)
    user_rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

