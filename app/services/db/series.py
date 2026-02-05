from app.extensions import db
from sqlalchemy import text
from datetime import datetime

# ============================================================
# Series - Check Status
# ============================================================

def is_series_in_progress(user_id: int, api_serie_id: int) -> bool:
    """
    Checks if a series is already in the user's progress/seen list.
    """
    if not user_id or not api_serie_id:
        return False
    
    try:
        result = db.session.execute(
            text("SELECT 1 FROM user_series_progress WHERE user_id=:user_id AND api_serie_id=:api_serie_id"),
            {"user_id": user_id, "api_serie_id": api_serie_id}
        )
        return result.fetchone() is not None
    except Exception:
        return False


def is_series_in_watchlist(user_id: int, api_serie_id: int) -> bool:
    """
    Checks if a series is already in the user's watchlist.
    """
    if not user_id or not api_serie_id:
        return False
    
    try:
        result = db.session.execute(
            text("SELECT 1 FROM user_series_watchlist WHERE user_id=:user_id AND api_serie_id=:api_serie_id"),
            {"user_id": user_id, "api_serie_id": api_serie_id}
        )
        return result.fetchone() is not None
    except Exception:
        return False


# ============================================================
# Series - Progress (Seen)
# ============================================================

def add_series_to_progress(user_id: int, api_serie_id: int, last_season_seen: int = 1, status: str = "Watching", rating: float = None):
    """
    Adds a series to the user's progress tracking.
    Tracks which season they're on, their watching status, and optional rating.
    Status options: "New Season Available", "Seen", "Watching"
    """
    if not user_id or not api_serie_id:
        return False
    
    try:
        db.session.execute(
            text("INSERT INTO user_series_progress (user_id, api_serie_id, last_season_seen, status, user_rating) VALUES (:user_id, :api_serie_id, :last_season_seen, :status, :user_rating)"),
            {"user_id": user_id, "api_serie_id": api_serie_id, "last_season_seen": last_season_seen, "status": status, "user_rating": rating}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def remove_series_from_progress(user_id: int, api_serie_id: int):
    """
    Removes a series from the user's progress tracking.
    """
    if not user_id or not api_serie_id:
        return False
    
    try:
        db.session.execute(
            text("DELETE FROM user_series_progress WHERE user_id=:user_id AND api_serie_id=:api_serie_id"),
            {"user_id": user_id, "api_serie_id": api_serie_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def update_series_progress(user_id: int, api_serie_id: int, last_season_seen: int = None, status: str = None, rating: float = None):
    """
    Updates series progress with any combination of: season, status, or rating.
    Only updates the fields that are provided (not None).
    """
    if not user_id or not api_serie_id:
        return False
    
    # Build dynamic update query
    updates = []
    params = {"user_id": user_id, "api_serie_id": api_serie_id}
    
    if last_season_seen is not None:
        updates.append("last_season_seen=:last_season_seen")
        params["last_season_seen"] = last_season_seen
    
    if status is not None:
        updates.append("status=:status")
        params["status"] = status
    
    if rating is not None:
        updates.append("user_rating=:user_rating")
        params["user_rating"] = rating
    
    if not updates:
        return False
    
    query = f"UPDATE user_series_progress SET {', '.join(updates)} WHERE user_id=:user_id AND api_serie_id=:api_serie_id"
    
    try:
        db.session.execute(text(query), params)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def update_series_status(user_id: int, api_serie_id: int, status: str):
    """
    Updates only the watching status for a series.
    Status options: "New Season Available", "Seen", "Watching"
    """
    if not user_id or not api_serie_id or not status:
        return False
    
    try:
        db.session.execute(
            text("UPDATE user_series_progress SET status=:status WHERE user_id=:user_id AND api_serie_id=:api_serie_id"),
            {"status": status, "user_id": user_id, "api_serie_id": api_serie_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def update_series_season(user_id: int, api_serie_id: int, last_season_seen: int):
    """
    Updates the last season seen for a series.
    """
    if not user_id or not api_serie_id or last_season_seen is None:
        return False
    
    try:
        db.session.execute(
            text("UPDATE user_series_progress SET last_season_seen=:last_season_seen WHERE user_id=:user_id AND api_serie_id=:api_serie_id"),
            {"last_season_seen": last_season_seen, "user_id": user_id, "api_serie_id": api_serie_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def update_series_rating(user_id: int, api_serie_id: int, new_rating: float):
    """
    Updates the user's rating for a series.
    Rating should be between 0.0 and 10.0.
    """
    if not user_id or not api_serie_id:
        return False
    
    try:
        db.session.execute(
            text("UPDATE user_series_progress SET user_rating=:user_rating WHERE user_id=:user_id AND api_serie_id=:api_serie_id"),
            {"user_rating": new_rating, "user_id": user_id, "api_serie_id": api_serie_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def get_series_watched(user_id: int, last_serie_id: int = None, last_date: datetime = None, limit: int = 30):
    """Get paginated series from user's progress/watched list, ordered by updated_at DESC."""
    if not user_id:
        return []
    
    try:
        if not (last_serie_id is not None and last_date is not None):
            query = """
                    SELECT api_serie_id, last_season_seen, status, user_rating, updated_at
                    FROM user_series_progress
                    WHERE user_id=:user_id
                    ORDER BY updated_at DESC, api_serie_id DESC
                    LIMIT :limit
                """
            res = db.session.execute(text(query), {"user_id": user_id, "limit": limit})
        else:
            query = """
                    SELECT api_serie_id, last_season_seen, status, user_rating, updated_at
                    FROM user_series_progress
                    WHERE user_id=:user_id AND (updated_at < :last_date OR (updated_at = :last_date AND api_serie_id < :last_serie_id))
                    ORDER BY updated_at DESC, api_serie_id DESC
                    LIMIT :limit
                """
            res = db.session.execute(text(query), {"user_id": user_id, "last_date": last_date, "last_serie_id": last_serie_id, "limit": limit})
        
        results = [dict(row._mapping) for row in res]
        return results
    
    except Exception:
        return []


# ============================================================
# Series - Watchlist
# ============================================================

def add_series_to_watchlist(user_id: int, api_serie_id: int):
    """
    Adds a series to the user's watchlist.
    """
    if not user_id or not api_serie_id:
        return False
    
    try:
        db.session.execute(
            text("INSERT INTO user_series_watchlist (user_id, api_serie_id) VALUES (:user_id, :api_serie_id)"),
            {"user_id": user_id, "api_serie_id": api_serie_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def remove_series_from_watchlist(user_id: int, api_serie_id: int):
    """
    Removes a series from the user's watchlist.
    """
    if not user_id or not api_serie_id:
        return False
    
    try:
        db.session.execute(
            text("DELETE FROM user_series_watchlist WHERE user_id=:user_id AND api_serie_id=:api_serie_id"),
            {"user_id": user_id, "api_serie_id": api_serie_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def get_series_watchlist(user_id: int, last_serie_id: int = None, last_date: datetime = None, limit: int = 30):
    """Get paginated series from user's watchlist, ordered by updated_at DESC."""
    if not user_id:
        return []
    
    try:
        if not (last_serie_id is not None and last_date is not None):
            query = """
                    SELECT api_serie_id, updated_at
                    FROM user_series_watchlist
                    WHERE user_id=:user_id
                    ORDER BY updated_at DESC, api_serie_id DESC
                    LIMIT :limit
                """
            res = db.session.execute(text(query), {"user_id": user_id, "limit": limit})
        else:
            query = """
                    SELECT api_serie_id, updated_at
                    FROM user_series_watchlist
                    WHERE user_id=:user_id AND (updated_at < :last_date OR (updated_at = :last_date AND api_serie_id < :last_serie_id))
                    ORDER BY updated_at DESC, api_serie_id DESC
                    LIMIT :limit
                """
            res = db.session.execute(text(query), {"user_id": user_id, "last_date": last_date, "last_serie_id": last_serie_id, "limit": limit})
        
        results = [dict(row._mapping) for row in res]
        return results
    
    except Exception:
        return []