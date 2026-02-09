from flask import Blueprint, render_template
from flask_login import login_required
from app.services.db import get_movies_watched, get_series_watched
from app.utils.title_helpers import (
    get_paginated_titles,
    get_similar_titles_for_user,
    get_recommendations_for_user,
)

watched_bp = Blueprint("watched", __name__, template_folder="../templates/watched")


@watched_bp.route("/watched", methods=["GET", "POST"])
@login_required
def watched():
    return render_template("watched.html", page="watched")


@watched_bp.route("/watched/movies", methods=["POST"])
@login_required
def get_watched_movies():
    """Get paginated list of watched movies with title information."""
    return get_paginated_titles(
        db_fetch_fn=get_movies_watched,
        media_type="movie",
        id_field="api_movie_id",
        error_msg="Failed to fetch watched movies",
    )


@watched_bp.route("/watched/series", methods=["POST"])
@login_required
def get_watched_series():
    """Get paginated list of watched series with title information."""
    return get_paginated_titles(
        db_fetch_fn=get_series_watched,
        media_type="tv",
        id_field="api_serie_id",
        error_msg="Failed to fetch watched series",
    )


@watched_bp.route("/watched/similar", methods=["POST"])
@login_required
def get_similar_from_watched():
    """Get similar titles based on a random watched title (movie or series)."""
    return get_similar_titles_for_user(
        get_movies_fn=get_movies_watched,
        get_series_fn=get_series_watched,
        error_msg="Failed to fetch similar titles",
    )


@watched_bp.route("/watched/recommendations", methods=["POST"])
@login_required
def get_recommendations_from_watched():
    """Get recommendations based on random watched titles (movies and series)."""
    return get_recommendations_for_user(
        get_movies_fn=get_movies_watched,
        get_series_fn=get_series_watched,
        error_msg="Failed to fetch recommendations",
    )

