from app.extensions import db
from app.extensions import bcrypt
from sqlalchemy import text

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
        text("SELECT movie_id FROM user_movies_seen WHERE user_id=:user_id"),
        {"user_id": user_id}
    )
    movies_seen = {row.movie_id for row in result}

    # Movies watchlist
    result = db.session.execute(
        text("SELECT movie_id FROM user_movies_watchlist WHERE user_id=:user_id"),
        {"user_id": user_id}
    )
    movies_watchlist = {row.movie_id for row in result}

    # Series seen
    result = db.session.execute(
        text("SELECT serie_id FROM user_series_seen WHERE user_id=:user_id"),
        {"user_id": user_id}
    )
    series_seen = {row.serie_id for row in result}

    # Series watchlist
    result = db.session.execute(
        text("SELECT serie_id FROM user_series_watchlist WHERE user_id=:user_id"),
        {"user_id": user_id}
    )
    series_watchlist = {row.serie_id for row in result}

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
            text("SELECT date, obs, rating FROM user_movies_seen WHERE user_id=:user_id AND movie_id=:id"),
            {"user_id": user_id, "id": id}
        )
        seen = [dict(row) for row in result]

        result = db.session.execute(
            text("SELECT movie_id FROM user_movies_watchlist WHERE user_id=:user_id AND movie_id=:id"),
            {"user_id": user_id, "id": id}
        )
        watchlist = bool(result.first())

    elif type == "tv":
        result = db.session.execute(
            text("SELECT serie_id, date, obs, rating FROM user_series_seen WHERE user_id=:user_id AND serie_id=:id"),
            {"user_id": user_id, "id": id}
        )
        seen = [dict(row) for row in result]

        result = db.session.execute(
            text("SELECT serie_id FROM user_series_watchlist WHERE user_id=:user_id AND serie_id=:id"),
            {"user_id": user_id, "id": id}
        )
        watchlist = bool(result.first())

    return {"seen": seen, "watchlist": watchlist}

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
        return False

    return True