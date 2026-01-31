from app.extensions import db
from app.extensions import bcrypt
from sqlalchemy import text

# User - titles

def fetch_user_marks_id(user_id: int, tmdb_ids: list[int]):
    """
        Returns any relation between the user and the title's ID's provided,
        such as if the title has been seen or is in a watchlist
    """
    movies_seen = set()
    movies_watchlist = set()
    series_seen = set()
    series_watchlist = set()

    if not tmdb_ids:
        return {
            "movies_seen": movies_seen,
            "movies_watchlist": movies_watchlist,
            "series_seen": series_seen,
            "series_watchlist": series_watchlist
        }

    # Movies seen
    result = db.session.execute(
        text("SELECT api_movie_id FROM user_movies_seen WHERE user_id=:user_id"),
        {"user_id": user_id}
    )
    movies_seen = {row.api_movie_id for row in result}

    # Movies watchlist
    result = db.session.execute(
        text("SELECT api_movie_id FROM user_movies_watchlist WHERE user_id=:user_id"),
        {"user_id": user_id}
    )
    movies_watchlist = {row.api_movie_id for row in result}

    # Series seen (from user_series_progress)
    result = db.session.execute(
        text("SELECT api_serie_id FROM user_series_progress WHERE user_id=:user_id"),
        {"user_id": user_id}
    )
    series_seen = {row.api_serie_id for row in result}

    # Series watchlist
    result = db.session.execute(
        text("SELECT api_serie_id FROM user_series_watchlist WHERE user_id=:user_id"),
        {"user_id": user_id}
    )
    series_watchlist = {row.api_serie_id for row in result}

    return {
        "movies_seen": movies_seen,
        "movies_watchlist": movies_watchlist,
        "series_seen": series_seen,
        "series_watchlist": series_watchlist
    }

def fetch_user_marks(user_id: int, id: int, type: str):
    """Returns all data in a user to a certain title relation"""
    if not id or not user_id:
        return {"seen": [], "watchlist": False}

    seen = []
    watchlist = False

    if type == "movie":
        result = db.session.execute(
            text("SELECT user_rating, updated_at FROM user_movies_seen WHERE user_id=:user_id AND api_movie_id=:id"),
            {"user_id": user_id, "id": id}
        )
        seen = [dict(row._mapping) for row in result]

        result = db.session.execute(
            text("SELECT api_movie_id FROM user_movies_watchlist WHERE user_id=:user_id AND api_movie_id=:id"),
            {"user_id": user_id, "id": id}
        )
        watchlist = bool(result.first())

    elif type == "tv":
        result = db.session.execute(
            text("SELECT api_serie_id, last_season_seen, status, user_rating, updated_at FROM user_series_progress WHERE user_id=:user_id AND api_serie_id=:id"),
            {"user_id": user_id, "id": id}
        )
        seen = [dict(row._mapping) for row in result]

        result = db.session.execute(
            text("SELECT api_serie_id FROM user_series_watchlist WHERE user_id=:user_id AND api_serie_id=:id"),
            {"user_id": user_id, "id": id}
        )
        watchlist = bool(result.first())

    return {"seen": seen, "watchlist": watchlist}

# Movies

def add_movie_to_seen(user_id: int, api_movie_id: int, rating: float = None):
    pass

def remove_movie_from_seen(user_id: int, api_movie_id: int):
    pass

def update_movie_rating(user_id: int, api_movie_id: int, new_rating: float):
    pass

# Series

def add_series_to_progress(user_id: int, api_serie_id: int, season: int, status: str, rating: float = None):
    pass

def update_series_status(user_id: int, api_serie_id: int, season: int, status: str):
    pass

def update_series_season(user_id: int, api_serie_id: int, last_season_seen: int):
    pass

# User only

def register_new_user(username, name, pw):
    if not username or not name or not pw:
        return False
    hashed_password = bcrypt.generate_password_hash(pw).decode("utf-8")
    try:
        db.session.execute(
            text("INSERT INTO users (name, username, pass_hash) VALUES (:name, :username, :pass_hash)"), 
            {"name": name, "username": username, "pass_hash": hashed_password}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False

    return True

def change_user_password(user_id: int, new_pw: str):
    if not user_id or not new_pw:
        return False
    
    hashed_password = bcrypt.generate_password_hash(new_pw).decode("utf-8")
    try:
        db.session.execute(
            text("UPDATE users SET pass_hash=:pass_hash WHERE id=:user_id"),
            {"pass_hash": hashed_password, "user_id": user_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def change_user_username(user_id: int, new_username: str):
    if not user_id or not new_username:
        return False
    
    try:
        db.session.execute(
            text("UPDATE users SET username=:new_username WHERE id=:user_id"),
            {"new_username": new_username, "user_id": user_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False
    
    return True

def username_available(username):
    try:
        result = db.session.execute(
            text("SELECT username FROM users WHERE username=:username"),
            {"username": username}
        )
        row = result.first()
        if row and row.username:
            return False
        return True
    except Exception:
        return False

def get_user_pfp(user_id: int):
    """Get the user's profile picture from the database"""
    if not user_id:
        return None
    try:
        result = db.session.execute(
            text("SELECT pfp FROM users WHERE id=:user_id"),
            {"user_id": user_id}
        )
        row = result.first()
        if row and row.pfp:
            return row.pfp
        return None
    except Exception:
        return None

def update_user_pfp(user_id: int, pfp_data: bytes):
    """Update the user's profile picture in the database"""
    if not user_id or not pfp_data:
        return False
    try:
        db.session.execute(
            text("UPDATE users SET pfp=:pfp WHERE id=:user_id"),
            {"pfp": pfp_data, "user_id": user_id}
        )
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False
    
# Notifications

def create_notifications(user_id: int, n_type: str, message: str, target_url: str = None):
    pass

def get_user_notifications(user_id: int, only_unread: bool = True):
    pass

def mark_notifications_as_read(user_id: int, notification_id: int):
    pass

def delete_old_notifications(user_id: int, days: int = 30):
    pass

# Stats

def get_user_stats(user_id: int):
    pass

def get_recent_activity(user_id: int, limit: int = 10):
    pass