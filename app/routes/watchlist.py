from flask import Blueprint, render_template
from flask_login import login_required
from app.services.db import get_movies_watchlist, get_series_watchlist, get_movies_watched, get_series_watched
from app.utils.title_helpers import (
    get_paginated_titles,
    get_similar_titles_for_user,
    get_recommendations_for_user,
)

watchlist_bp = Blueprint("watchlist", __name__, template_folder="../templates/watchlist")


@watchlist_bp.route("/watchlist", methods=["GET", "POST"])
@login_required
def watchlist():
    return render_template("watchlist.html", page="watchlist")


@watchlist_bp.route("/watchlist/movies", methods=["POST"])
@login_required
def get_watchlist_movies():
    """Get paginated list of movies in watchlist with title information."""
    return get_paginated_titles(
        db_fetch_fn=get_movies_watchlist,
        media_type="movie",
        id_field="api_movie_id",
        error_msg="Failed to fetch watchlist movies",
    )


@watchlist_bp.route("/watchlist/series", methods=["POST"])
@login_required
def get_watchlist_series():
    """Get paginated list of series in watchlist with title information."""
    return get_paginated_titles(
        db_fetch_fn=get_series_watchlist,
        media_type="tv",
        id_field="api_serie_id",
        error_msg="Failed to fetch watchlist series",
    )


@watchlist_bp.route("/watchlist/similar", methods=["POST"])
@login_required
def get_similar_from_watchlist():
    """Get similar titles based on a random watched title (movie or series)."""
    return get_similar_titles_for_user(
        get_movies_fn=get_movies_watched,
        get_series_fn=get_series_watched,
        error_msg="Failed to fetch similar titles",
    )


@watchlist_bp.route("/watchlist/recommendations", methods=["POST"])
@login_required
def get_recommendations_from_watchlist():
    """Get recommendations based on random watched titles (movies and series)."""
    return get_recommendations_for_user(
        get_movies_fn=get_movies_watched,
        get_series_fn=get_series_watched,
        error_msg="Failed to fetch recommendations",
    )

