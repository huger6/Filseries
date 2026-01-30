from sqlalchemy import Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db

# Notification types
NOTIFICATION_TYPES = ("New Season Available", "Warning", "Suggestion", "Normal")


class Notification(db.Model):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    type: Mapped[str | None] = mapped_column(Enum(*NOTIFICATION_TYPES, name="notification_type"), nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
