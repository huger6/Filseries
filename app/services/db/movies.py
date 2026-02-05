from app.extensions import db
from sqlalchemy import text
from datetime import datetime

# ============================================================
# Movies - Check Status
# ============================================================

def is_movie_in_seen(user_id: int, api_movie_id: int) -> bool:
    """
    Checks if a movie is already in the user's seen list.
    """
    if not user_id or not api_movie_id:
        return False
    
    try:
        result = db.session.execute(
            text("SELECT 1 FROM user_movies_seen WHERE user_id=:user_id AND api_movie_id=:api_movie_id"),
            {"user_id": user_id, "api_movie_id": api_movie_id}
        )
        return result.fetchone() is not None
    except Exception:
        return False


def is_movie_in_watchlist(user_id: int, api_movie_id: int) -> bool:
    """
    Checks if a movie is already in the user's watchlist.
    """
    if not user_id or not api_movie_id:
        return False
    
    try:
        result = db.session.execute(
            text("SELECT 1 FROM user_movies_watchlist WHERE user_id=:user_id AND api_movie_id=:api_movie_id"),
            {"user_id": user_id, "api_movie_id": api_movie_id}
        )
        return result.fetchone() is not None
    except Exception:
        return False


# ============================================================
# Movies - Seen
# ============================================================

def add_movie_to_seen(user_id: int, api_movie_id: int, rating: float = None):
    """
    Marks a movie as seen by the user.
    Optionally includes a user rating (0.0-10.0).
    """
    if not user_id or not api_movie_id:
        return False
    
    try:
        db.session.execute(
            text("INSERT INTO user_movies_seen (user_id, api_movie_id, user_rating) VALUES (:user_id, :api_movie_id, :user_rating)"),
            {"user_id": user_id, "api_movie_id": api_movie_id, "user_rating": rating}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def remove_movie_from_seen(user_id: int, api_movie_id: int):
    """
    Removes a movie from the user's seen list.
    """
    if not user_id or not api_movie_id:
        return False
    
    try:
        db.session.execute(
            text("DELETE FROM user_movies_seen WHERE user_id=:user_id AND api_movie_id=:api_movie_id"),
            {"user_id": user_id, "api_movie_id": api_movie_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def update_movie_rating(user_id: int, api_movie_id: int, new_rating: float):
    """
    Updates the user's rating for a seen movie.
    Rating should be between 0.0 and 10.0.
    """
    if not user_id or not api_movie_id:
        return False
    
    try:
        db.session.execute(
            text("UPDATE user_movies_seen SET user_rating=:user_rating WHERE user_id=:user_id AND api_movie_id=:api_movie_id"),
            {"user_rating": new_rating, "user_id": user_id, "api_movie_id": api_movie_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def get_movies_watched(user_id: int, last_movie_id: int = None, last_date: datetime = None, limit: int = 30):
    if not user_id:
        return []
    
    try:
        if not (last_movie_id is not None or last_date is not None):
            query = """
                    SELECT api_movie_id, user_rating, updated_at
                    FROM user_movies_seen
                    WHERE user_id=:user_id
                    ORDER BY updated_at DESC, api_movie_id DESC
                    LIMIT :limit
                """
            # Note: api_movie_id DESC to not randomise equal date chosen titles selection
            res = db.session.execute(text(query), {"user_id": user_id, "limit": limit})
        else:
            # Get only what comes after last title loaded
            query = """
                    SELECT api_movie_id, user_rating, updated_at
                    FROM user_movies_seen
                    WHERE user_id=:user_id AND (updated_at < :last_date OR (updated_at = :last_date AND api_movie_id < :last_movie_id))
                    ORDER BY updated_at DESC, api_movie_id DESC
                    LIMIT :limit
                """
            # Note: api_movie_id DESC to not randomise equal date chosen titles selection
            res = db.session.execute(text(query), {"user_id": user_id,"last_date": last_date, "last_movie_id": last_movie_id, "limit": limit})
        
        results = [dict(row._mapping) for row in res]
        return results
    
    except Exception:
        return []

# ============================================================
# Movies - Watchlist
# ============================================================

def add_movie_to_watchlist(user_id: int, api_movie_id: int):
    """
    Adds a movie to the user's watchlist.
    """
    if not user_id or not api_movie_id:
        return False
    
    try:
        db.session.execute(
            text("INSERT INTO user_movies_watchlist (user_id, api_movie_id) VALUES (:user_id, :api_movie_id)"),
            {"user_id": user_id, "api_movie_id": api_movie_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def remove_movie_from_watchlist(user_id: int, api_movie_id: int):
    """
    Removes a movie from the user's watchlist.
    """
    if not user_id or not api_movie_id:
        return False
    
    try:
        db.session.execute(
            text("DELETE FROM user_movies_watchlist WHERE user_id=:user_id AND api_movie_id=:api_movie_id"),
            {"user_id": user_id, "api_movie_id": api_movie_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def get_movies_watchlist(user_id: int, last_movie_id: int = None, last_date: datetime = None, limit: int = 30):
    """Get paginated movies from user's watchlist, ordered by updated_at DESC."""
    if not user_id:
        return []
    
    try:
        if not (last_movie_id is not None and last_date is not None):
            query = """
                    SELECT api_movie_id, updated_at
                    FROM user_movies_watchlist
                    WHERE user_id=:user_id
                    ORDER BY updated_at DESC, api_movie_id DESC
                    LIMIT :limit
                """
            res = db.session.execute(text(query), {"user_id": user_id, "limit": limit})
        else:
            query = """
                    SELECT api_movie_id, updated_at
                    FROM user_movies_watchlist
                    WHERE user_id=:user_id AND (updated_at < :last_date OR (updated_at = :last_date AND api_movie_id < :last_movie_id))
                    ORDER BY updated_at DESC, api_movie_id DESC
                    LIMIT :limit
                """
            res = db.session.execute(text(query), {"user_id": user_id, "last_date": last_date, "last_movie_id": last_movie_id, "limit": limit})
        
        results = [dict(row._mapping) for row in res]
        return results
    
    except Exception:
        return []
