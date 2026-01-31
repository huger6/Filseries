from app.extensions import db
from sqlalchemy import text

# ============================================================
# User Statistics
# ============================================================

def get_user_stats(user_id: int):
    """
    Retrieves aggregated statistics for a user's profile.
    Returns counts for movies seen, series in progress, and items in watchlist.
    """
    if not user_id:
        return {"movies_seen": 0, "series_watched": 0, "watchlist_count": 0}
    
    try:
        # Count movies seen
        result = db.session.execute(
            text("SELECT COUNT(*) as count FROM user_movies_seen WHERE user_id=:user_id"),
            {"user_id": user_id}
        )
        movies_seen = result.first().count
        
        # Count series in progress
        result = db.session.execute(
            text("SELECT COUNT(*) as count FROM user_series_progress WHERE user_id=:user_id AND status='Seen'"),
            {"user_id": user_id}
        )
        series_watched = result.first().count
        
        # Count total watchlist items (movies + series)
        result = db.session.execute(
            text("SELECT (SELECT COUNT(*) FROM user_movies_watchlist WHERE user_id=:user_id) + (SELECT COUNT(*) FROM user_series_watchlist WHERE user_id=:user_id) as count"),
            {"user_id": user_id}
        )
        watchlist_count = result.first().count
        
        return {
            "movies_seen": movies_seen,
            "series_watched": series_watched,
            "watchlist_count": watchlist_count
        }
    except Exception:
        return {"movies_seen": 0, "series_watched": 0, "watchlist_count": 0}

def get_recent_activity(user_id: int, limit: int = 10):
    """
    Retrieves the user's most recent activity across all title types.
    Combines movies seen, series progress, and watchlist additions.
    Returns a list ordered by most recent activity first.
    """
    if not user_id or limit < 1:
        return []
    
    try:
        # Union query to get recent activity from all tables
        query = """
            (SELECT 'movie_seen' as activity_type, api_movie_id as title_id, NULL as extra_info, updated_at 
             FROM user_movies_seen WHERE user_id=:user_id)
            UNION ALL
            (SELECT 'series_progress' as activity_type, api_serie_id as title_id, CONCAT('S', last_season_seen, ' - ', status) as extra_info, updated_at 
             FROM user_series_progress WHERE user_id=:user_id)
            UNION ALL
            (SELECT 'movie_watchlist' as activity_type, api_movie_id as title_id, NULL as extra_info, updated_at 
             FROM user_movies_watchlist WHERE user_id=:user_id)
            UNION ALL
            (SELECT 'series_watchlist' as activity_type, api_serie_id as title_id, NULL as extra_info, updated_at 
             FROM user_series_watchlist WHERE user_id=:user_id)
            ORDER BY updated_at DESC
            LIMIT :limit
        """
        
        result = db.session.execute(text(query), {"user_id": user_id, "limit": limit})
        activity = [dict(row._mapping) for row in result]
        return activity
    except Exception:
        return []
