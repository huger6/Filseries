from app.extensions import db
from sqlalchemy import text

# ============================================================
# User - Titles Relationship Queries
# ============================================================

def fetch_user_marks_id(user_id: int, tmdb_ids: list[int]):
    """
    Fetches all title IDs that the user has marked as seen or added to watchlist.
    Used for displaying status indicators on title cards in lists/grids.
    Returns sets of movie/series IDs for seen and watchlist categories.
    """
    movies_seen = set()
    movies_watchlist = set()
    series_seen = set()
    series_watchlist = set()

    if not user_id or not tmdb_ids:
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
    """
    Fetches detailed user data for a specific title (movie or series).
    Returns seen status with rating/progress info and watchlist status.
    Used on individual title detail pages.
    """
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

