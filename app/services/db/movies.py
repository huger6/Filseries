from app.extensions import db
from sqlalchemy import text

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

