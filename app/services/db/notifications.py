from app.extensions import db
from sqlalchemy import text

# ============================================================
# Notifications
# ============================================================

def create_notification(user_id: int, n_type: str, message: str, target_url: str = None):
    """
    Creates a new notification for a user.
    Types: "New Season Available", "Warning", "Suggestion", "Normal"
    target_url is optional and used for clickable notifications.
    """
    if not user_id or not n_type or not message:
        return False
    
    try:
        db.session.execute(
            text("INSERT INTO notifications (user_id, type, message, target_url) VALUES (:user_id, :type, :message, :target_url)"),
            {"user_id": user_id, "type": n_type, "message": message, "target_url": target_url}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def get_user_notifications(user_id: int, only_unread: bool = True):
    """
    Retrieves notifications for a user, ordered by most recent.
    If only_unread is True, returns only unread notifications.
    Returns empty list on error.
    """
    if not user_id:
        return []
    
    try:
        if only_unread:
            query = "SELECT id, type, message, target_url, is_read, created_at FROM notifications WHERE user_id=:user_id AND is_read=FALSE ORDER BY created_at DESC"
        else:
            query = "SELECT id, type, message, target_url, is_read, created_at FROM notifications WHERE user_id=:user_id ORDER BY created_at DESC"
        
        result = db.session.execute(text(query), {"user_id": user_id})
        notifications = [dict(row._mapping) for row in result]
        return notifications
    except Exception:
        return []

def mark_notification_as_read(user_id: int, notification_id: int):
    """
    Marks a specific notification as read.
    Validates that the notification belongs to the user.
    """
    if not user_id or not notification_id:
        return False
    
    try:
        db.session.execute(
            text("UPDATE notifications SET is_read=TRUE WHERE user_id=:user_id AND id=:notification_id"),
            {"user_id": user_id, "notification_id": notification_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def mark_all_notifications_as_read(user_id: int):
    """
    Marks all notifications for a user as read.
    """
    if not user_id:
        return False
    
    try:
        db.session.execute(
            text("UPDATE notifications SET is_read=TRUE WHERE user_id=:user_id"),
            {"user_id": user_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def delete_notification(user_id: int, notification_id: int):
    """
    Deletes a specific notification.
    Validates that the notification belongs to the user.
    """
    if not user_id or not notification_id:
        return False
    
    try:
        db.session.execute(
            text("DELETE FROM notifications WHERE user_id=:user_id AND id=:notification_id"),
            {"user_id": user_id, "notification_id": notification_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def delete_old_notifications(user_id: int, days: int = 30):
    """
    Deletes notifications older than the specified number of days.
    Default is 30 days. Only deletes read notifications.
    """
    if not user_id or days < 0:
        return False
    
    try:
        db.session.execute(
            text("DELETE FROM notifications WHERE user_id=:user_id AND is_read=TRUE AND created_at < DATE_SUB(NOW(), INTERVAL :days DAY)"),
            {"user_id": user_id, "days": days}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def get_unread_notification_count(user_id: int):
    """
    Returns the count of unread notifications for a user.
    Used for displaying notification badges.
    """
    if not user_id:
        return 0
    
    try:
        result = db.session.execute(
            text("SELECT COUNT(*) as count FROM notifications WHERE user_id=:user_id AND is_read=FALSE"),
            {"user_id": user_id}
        )
        row = result.first()
        return row.count if row else 0
    except Exception:
        return 0
