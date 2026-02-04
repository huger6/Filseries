from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.services.db import (
    add_series_to_watchlist,
    add_series_to_progress,
    remove_series_from_progress,
    remove_series_from_watchlist,
    update_series_progress,
    update_series_season,
    update_series_rating,
    update_series_status,
    is_series_in_progress,
    is_series_in_watchlist
)
from app.validations import validate_title_id, validate_season_number, validate_rating
from app.exceptions import StatusError

serie_bp = Blueprint("series", __name__, template_folder="../templates/series")

# ============================================================
# Series - In progress
# ============================================================

@serie_bp.route("/tv/progress/add", methods=["POST"])
@login_required
def add_serie_to_progress():
    """Add a series to the user's progress/watching list"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    series_id = data.get("id")
    season_number = data.get("season_number", 1)  # Default to season 1
    
    # Validate input
    try:
        validate_title_id(series_id)
        validate_season_number(season_number)
    except StatusError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
    user_id = current_user.id

    # Check if series is already in progress list
    if is_series_in_progress(user_id, series_id):
        return jsonify({"success": False, "message": "This series is already in your watching list."}), 400

    # Check if series is in watchlist and remove it
    if is_series_in_watchlist(user_id, series_id):
        remove_series_from_watchlist(user_id=user_id, api_serie_id=series_id)

    # Insert data
    try:
        res = add_series_to_progress(user_id=user_id, api_serie_id=series_id, last_season_seen=season_number)
        if res:
            return jsonify({"success": True, "message": "Series added to your watching list."}), 200
        else:
            return jsonify({"success": False, "message": "Failed to add series to watching list."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@serie_bp.route("/tv/progress/remove", methods=["POST"])
@login_required
def remove_serie_from_progress():
    """Remove a series from the user's progress/watching list"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    series_id = data.get("id")
    
    # Validate input
    try:
        validate_title_id(series_id)
    except StatusError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
    user_id = current_user.id

    # Remove data
    try:
        res = remove_series_from_progress(user_id=user_id, api_series_id=series_id)
        if res:
            return jsonify({"success": True, "message": "Series removed from your watching list."}), 200
        else:
            return jsonify({"success": False, "message": "Failed to remove series from watching list."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@serie_bp.route("/tv/progress/update", methods=["POST"])
@login_required
def update_serie_progress():
    """Update a series progress (season number)"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    series_id = data.get("id")
    season_number = data.get("season_number")
    
    # Validate input
    try:
        validate_title_id(series_id)
        validate_season_number(season_number)
    except StatusError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
    user_id = current_user.id

    # Update data
    try:
        res = update_series_progress(user_id=user_id, api_series_id=series_id, season_number=season_number)
        if res:
            return jsonify({"success": True, "message": f"Progress updated to season {season_number}."}), 200
        else:
            return jsonify({"success": False, "message": "Failed to update series progress."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@serie_bp.route("/tv/progress/update/status", methods=["POST"])
@login_required
def update_serie_status():
    """Update a series status (watching, completed, on-hold, dropped)"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    series_id = data.get("id")
    status = data.get("status")
    
    # Validate input
    try:
        validate_title_id(series_id)
        if not status or status not in ["watching", "completed", "on-hold", "dropped"]:
            raise StatusError("Invalid status. Must be: watching, completed, on-hold, or dropped")
    except StatusError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
    user_id = current_user.id

    # Update data
    try:
        res = update_series_status(user_id=user_id, api_series_id=series_id, status=status)
        if res:
            return jsonify({"success": True, "message": f"Status updated to {status}."}), 200
        else:
            return jsonify({"success": False, "message": "Failed to update series status."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@serie_bp.route("/tv/progress/update/last-season-seen", methods=["POST"])
@login_required
def update_serie_last_season_seen():
    """Update the last season seen for a series"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    series_id = data.get("series_id")
    season_number = data.get("season_number")
    
    # Validate input
    try:
        validate_title_id(series_id)
        validate_season_number(season_number)
    except StatusError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
    user_id = current_user.id

    try:
        res = update_series_season(user_id=user_id, api_series_id=series_id, season_number=season_number)
        if res:
            return jsonify({
                "success": True, 
                "message": f"Last season seen updated to Season {season_number}",
                "season_number": season_number
            }), 200
        else:
            return jsonify({"success": False, "message": "Failed to update last season seen."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@serie_bp.route("/tv/progress/update/rating", methods=["POST"])
@login_required
def update_serie_rating():
    """Update a series rating"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    series_id = data.get("id")
    rating = data.get("rating")
    
    # Validate input
    try:
        validate_title_id(series_id)
        validate_rating(rating)
    except StatusError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
    user_id = current_user.id

    # Update data
    try:
        res = update_series_rating(user_id=user_id, api_series_id=series_id, rating=rating)
        if res:
            return jsonify({"success": True, "message": "Rating updated."}), 200
        else:
            return jsonify({"success": False, "message": "Failed to update series rating."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ============================================================
# Series - Watchlist
# ============================================================

@serie_bp.route("/tv/watchlist/add", methods=["POST"])
@login_required
def add_series_watchlist():
    """Add a series to the user's watchlist"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    series_id = data.get("id")
    
    # Validate input
    try:
        validate_title_id(series_id)
    except StatusError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
    user_id = current_user.id

    # Check if series is already in progress list (can't add to watchlist if already watching)
    if is_series_in_progress(user_id, series_id):
        return jsonify({"success": False, "message": "This series is already in your watching list."}), 400

    # Check if series is already in watchlist
    if is_series_in_watchlist(user_id, series_id):
        return jsonify({"success": False, "message": "This series is already in your watchlist."}), 400

    # Insert data
    try:
        res = add_series_to_watchlist(user_id=user_id, api_serie_id=series_id)
        if res:
            return jsonify({"success": True, "message": "Series added to your watchlist."}), 200
        else:
            return jsonify({"success": False, "message": "Failed to add series to watchlist."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@serie_bp.route("/tv/watchlist/remove", methods=["POST"])
@login_required
def remove_series_watchlist():
    """Remove a series from the user's watchlist"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    series_id = data.get("id")
    
    # Validate input
    try:
        validate_title_id(series_id)
    except StatusError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
    user_id = current_user.id

    # Remove data
    try:
        res = remove_series_from_watchlist(user_id=user_id, api_serie_id=series_id)
        if res:
            return jsonify({"success": True, "message": "Series removed from your watchlist."}), 200
        else:
            return jsonify({"success": False, "message": "Failed to remove series from watchlist."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
