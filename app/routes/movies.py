from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.services.db import (
    add_movie_to_watchlist,
    add_movie_to_seen,
    remove_movie_from_seen,
    remove_movie_from_watchlist,
    remove_movie_from_watchlist,
    update_movie_rating,
    is_movie_in_seen,
    is_movie_in_watchlist
)
from app.validations import validate_title_id, validate_rating
from app.exceptions import StatusError, StatusUnchanged


movie_bp = Blueprint("movies", __name__, template_folder="../templates/movies")

# ============================================================
# Movies - Seen
# ============================================================

@movie_bp.route("/movies/seen/add", methods=["POST"])
@login_required
def add_movie_seen():
    """Add a movie to the user's seen list"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    movie_id = data.get("id")
    
    # Validate input
    try:
        validate_title_id(movie_id)
    except StatusError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
    user_id = current_user.id

    # Check if movie is already in seen list
    if is_movie_in_seen(user_id, movie_id):
        return jsonify({"success": False, "message": "This movie is already in your seen list."}), 400

    # Check if movie is in watchlist and remove it
    if is_movie_in_watchlist(user_id, movie_id):
        remove_movie_from_watchlist(user_id=user_id, api_movie_id=movie_id)

    # Insert data
    try:
        res = add_movie_to_seen(user_id=user_id, api_movie_id=movie_id)
        if res:
            return jsonify({"success": True, "message": "Movie added to your seen list."}), 200
        else:
            return jsonify({"success": False, "message": "Failed to add movie to seen list."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@movie_bp.route("/movies/seen/remove", methods=["POST"])
@login_required
def remove_movie_seen():
    """Remove a movie from the user's seen list"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    movie_id = data.get("id")
    
    # Validate input
    try:
        validate_title_id(movie_id)
    except StatusError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
    user_id = current_user.id

    # Check if movie is in seen list before removing
    if not is_movie_in_seen(user_id, movie_id):
        return jsonify({"success": False, "message": "This movie is not in your seen list."}), 404

    # Remove data
    try:
        res = remove_movie_from_seen(user_id=user_id, api_movie_id=movie_id)
        if res:
            return jsonify({"success": True, "message": "Movie removed from your seen list."}), 200
        else:
            return jsonify({"success": False, "message": "Failed to remove movie from seen list."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@movie_bp.route("/movies/seen/update", methods=["POST"])
@login_required
def update_movie_seen():
    """Update a movie's rating in the user's seen list"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    movie_id = data.get("id")
    rating = data.get("rating")
    
    # Validate input
    try:
        validate_title_id(movie_id)
        validate_rating(rating)
    except StatusError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
    user_id = current_user.id

    # Check if movie is in seen list before updating
    if not is_movie_in_seen(user_id, movie_id):
        return jsonify({"success": False, "message": "This movie is not in your seen list."}), 404

    # Update data
    try:
        res = update_movie_rating(user_id=user_id, api_movie_id=movie_id, rating=rating)
        if res:
            return jsonify({"success": True, "message": "Movie rating updated."}), 200
        else:
            return jsonify({"success": False, "message": "Failed to update movie rating."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ============================================================
# Movies - Watchlist
# ============================================================

@movie_bp.route("/movies/watchlist/add", methods=["POST"])
@login_required
def add_movie_watchlist():
    """Add a movie to the user's watchlist"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    movie_id = data.get("id")
    
    # Validate input
    try:
        validate_title_id(movie_id)
    except StatusError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
    user_id = current_user.id

    # Check if movie is already in seen list (can't add to watchlist if already seen)
    if is_movie_in_seen(user_id, movie_id):
        return jsonify({"success": False, "message": "This movie is already marked as seen."}), 400

    # Check if movie is already in watchlist
    if is_movie_in_watchlist(user_id, movie_id):
        return jsonify({"success": False, "message": "This movie is already in your watchlist."}), 400

    # Insert data
    try:
        res = add_movie_to_watchlist(user_id=user_id, api_movie_id=movie_id)
        if res:
            return jsonify({"success": True, "message": "Movie added to your watchlist."}), 200
        else:
            return jsonify({"success": False, "message": "Failed to add movie to watchlist."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@movie_bp.route("/movies/watchlist/remove", methods=["POST"])
@login_required
def remove_movie_watchlist():
    """Remove a movie from the user's watchlist"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    movie_id = data.get("id")
    
    # Validate input
    try:
        validate_title_id(movie_id)
    except StatusError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
    user_id = current_user.id

    # Check if movie is in watchlist before removing
    if not is_movie_in_watchlist(user_id, movie_id):
        return jsonify({"success": False, "message": "This movie is not in your watchlist."}), 404

    # Remove data
    try:
        res = remove_movie_from_watchlist(user_id=user_id, api_movie_id=movie_id)
        if res:
            return jsonify({"success": True, "message": "Movie removed from your watchlist."}), 200
        else:
            return jsonify({"success": False, "message": "Failed to remove movie from watchlist."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
