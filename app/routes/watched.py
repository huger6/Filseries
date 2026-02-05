import asyncio
import random
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
import aiohttp
from app.services.db import get_movies_watched, get_movies_watchlist, get_series_watched, get_series_watchlist
from app.services.search_info import fetch_titles_info_batch
from app.services.api.api_info import get_similar_titles, get_recommendations
from app.validations import validate_pagination_params
from app.exceptions import StatusError
from app.constants import ALLOWED_FIELDS_SEARCH

watched_bp = Blueprint("watched", __name__, template_folder="../templates/watched")


def _merge_user_data(title_entry: dict, user_data: dict) -> dict:
    """Merge user-specific data (rating, status, etc.) into title entry."""
    if not user_data:
        return title_entry
    
    result = title_entry.copy()
    
    if "user_rating" in user_data:
        result["user_rating"] = user_data["user_rating"]
    if "updated_at" in user_data:
        result["updated_at"] = user_data["updated_at"].isoformat() if isinstance(user_data["updated_at"], datetime) else user_data["updated_at"]
    if "last_season_seen" in user_data:
        result["last_season_seen"] = user_data["last_season_seen"]
    if "status" in user_data:
        result["status"] = user_data["status"]
    
    return result


@watched_bp.route("/watched", methods=["GET", "POST"])
@login_required
def watched():
    return render_template("watched.html", page="watched")


@watched_bp.route("/watched/movies", methods=["POST"])
@login_required
def get_watched_movies():
    """Get paginated list of watched movies with title information."""
    data = request.get_json() or {}
    
    # Validate pagination parameters
    try:
        last_id, last_date, limit = validate_pagination_params(
            data.get("last_id"),
            data.get("last_date"),
            data.get("limit")
        )
    except StatusError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
    try:
        # Get movies from database
        db_results = get_movies_watched(
            user_id=current_user.id,
            last_movie_id=last_id,
            last_date=last_date,
            limit=limit
        )
        
        if not db_results:
            return jsonify({"success": True, "results": [], "has_more": False}), 200
        
        # Extract movie IDs and user data
        movie_ids = [r["api_movie_id"] for r in db_results]
        user_data_map = {r["api_movie_id"]: r for r in db_results}
        
        # Fetch title info from TMDB API
        title_info_map = asyncio.run(fetch_titles_info_batch(movie_ids, "movie"))
        
        # Process and combine results
        results = []
        for movie_id in movie_ids:
            title_data = title_info_map.get(movie_id)
            if title_data:
                processed = _merge_user_data(title_data, user_data_map.get(movie_id))
                results.append(processed)
        
        # Determine if there are more results
        has_more = len(db_results) >= limit
        
        return jsonify({
            "success": True,
            "results": results,
            "has_more": has_more
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": "Failed to fetch watched movies"}), 500


@watched_bp.route("/watched/series", methods=["POST"])
@login_required
def get_watched_series():
    """Get paginated list of watched series with title information."""
    data = request.get_json() or {}
    
    # Validate pagination parameters
    try:
        last_id, last_date, limit = validate_pagination_params(
            data.get("last_id"),
            data.get("last_date"),
            data.get("limit")
        )
    except StatusError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
    try:
        # Get series from database
        db_results = get_series_watched(
            user_id=current_user.id,
            last_serie_id=last_id,
            last_date=last_date,
            limit=limit
        )
        
        if not db_results:
            return jsonify({"success": True, "results": [], "has_more": False}), 200
        
        # Extract series IDs and user data
        series_ids = [r["api_serie_id"] for r in db_results]
        user_data_map = {r["api_serie_id"]: r for r in db_results}
        
        # Fetch title info from TMDB API
        title_info_map = asyncio.run(fetch_titles_info_batch(series_ids, "tv"))
        
        # Process and combine results
        results = []
        for series_id in series_ids:
            title_data = title_info_map.get(series_id)
            if title_data:
                processed = _merge_user_data(title_data, user_data_map.get(series_id))
                results.append(processed)
        
        # Determine if there are more results
        has_more = len(db_results) >= limit
        
        return jsonify({
            "success": True,
            "results": results,
            "has_more": has_more
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": "Failed to fetch watched series"}), 500


@watched_bp.route("/watchlist/movies", methods=["POST"])
@login_required
def get_watchlist_movies():
    """Get paginated list of movies in watchlist with title information."""
    data = request.get_json() or {}
    
    # Validate pagination parameters
    try:
        last_id, last_date, limit = validate_pagination_params(
            data.get("last_id"),
            data.get("last_date"),
            data.get("limit")
        )
    except StatusError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
    try:
        # Get movies from database
        db_results = get_movies_watchlist(
            user_id=current_user.id,
            last_movie_id=last_id,
            last_date=last_date,
            limit=limit
        )
        
        if not db_results:
            return jsonify({"success": True, "results": [], "has_more": False}), 200
        
        # Extract movie IDs and user data
        movie_ids = [r["api_movie_id"] for r in db_results]
        user_data_map = {r["api_movie_id"]: r for r in db_results}
        
        # Fetch title info from TMDB API
        title_info_map = asyncio.run(fetch_titles_info_batch(movie_ids, "movie"))
        
        # Process and combine results
        results = []
        for movie_id in movie_ids:
            title_data = title_info_map.get(movie_id)
            if title_data:
                processed = _merge_user_data(title_data, user_data_map.get(movie_id))
                results.append(processed)
        
        # Determine if there are more results
        has_more = len(db_results) >= limit
        
        return jsonify({
            "success": True,
            "results": results,
            "has_more": has_more
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": "Failed to fetch watchlist movies"}), 500


@watched_bp.route("/watchlist/series", methods=["POST"])
@login_required
def get_watchlist_series():
    """Get paginated list of series in watchlist with title information."""
    data = request.get_json() or {}
    
    # Validate pagination parameters
    try:
        last_id, last_date, limit = validate_pagination_params(
            data.get("last_id"),
            data.get("last_date"),
            data.get("limit")
        )
    except StatusError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
    try:
        # Get series from database
        db_results = get_series_watchlist(
            user_id=current_user.id,
            last_serie_id=last_id,
            last_date=last_date,
            limit=limit
        )
        
        if not db_results:
            return jsonify({"success": True, "results": [], "has_more": False}), 200
        
        # Extract series IDs and user data
        series_ids = [r["api_serie_id"] for r in db_results]
        user_data_map = {r["api_serie_id"]: r for r in db_results}
        
        # Fetch title info from TMDB API
        title_info_map = asyncio.run(fetch_titles_info_batch(series_ids, "tv"))
        
        # Process and combine results
        results = []
        for series_id in series_ids:
            title_data = title_info_map.get(series_id)
            if title_data:
                processed = _merge_user_data(title_data, user_data_map.get(series_id))
                results.append(processed)
        
        # Determine if there are more results
        has_more = len(db_results) >= limit
        
        return jsonify({
            "success": True,
            "results": results,
            "has_more": has_more
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": "Failed to fetch watchlist series"}), 500


def _filter_title_fields(title: dict, media_type: str) -> dict:
    """Filter title to only include allowed fields."""
    filtered = {k: v for k, v in title.items() if k in ALLOWED_FIELDS_SEARCH}
    filtered["media_type"] = media_type
    
    # Normalize title field for TV shows
    if media_type == "tv" and "name" in title:
        filtered["title"] = title["name"]
    
    # Normalize release_date for TV shows
    if media_type == "tv" and "first_air_date" in title:
        filtered["release_date"] = title["first_air_date"]
    
    return filtered


@watched_bp.route("/watched/similar", methods=["POST"])
@login_required
def get_similar_from_watched():
    """Get similar titles based on a random watched title (movie or series)."""
    try:
        # Get recently watched movies and series
        movies = get_movies_watched(
            user_id=current_user.id,
            last_movie_id=None,
            last_date=None,
            limit=15
        ) or []
        
        series = get_series_watched(
            user_id=current_user.id,
            last_serie_id=None,
            last_date=None,
            limit=15
        ) or []
        
        # Combine into a unified list with media_type info
        all_watched = []
        for m in movies:
            all_watched.append({"id": m["api_movie_id"], "media_type": "movie"})
        for s in series:
            all_watched.append({"id": s["api_serie_id"], "media_type": "tv"})
        
        if not all_watched:
            return jsonify({"success": True, "results": []}), 200
        
        # Get IDs of titles user has already watched to exclude them
        watched_movie_ids = {m["api_movie_id"] for m in movies}
        watched_series_ids = {s["api_serie_id"] for s in series}
        
        # Pick a random title from the user's watched list
        random_title = random.choice(all_watched)
        source_id = random_title["id"]
        source_media_type = random_title["media_type"]
        
        async def fetch_similar():
            async with aiohttp.ClientSession() as session:
                results = await get_similar_titles(session, source_id, source_media_type)
                return results or []
        
        similar_titles = asyncio.run(fetch_similar())
        
        # Get the appropriate watched IDs set based on media type
        watched_ids = watched_movie_ids if source_media_type == "movie" else watched_series_ids
        
        # Filter and limit results, excluding already watched titles
        filtered_results = []
        seen_ids = set()
        
        for title in similar_titles:
            title_id = title.get("id")
            if title_id not in seen_ids and title_id not in watched_ids:
                seen_ids.add(title_id)
                filtered_results.append(_filter_title_fields(title, source_media_type))
                if len(filtered_results) >= 30:
                    break
        
        return jsonify({
            "success": True,
            "results": filtered_results,
            "source_id": source_id,
            "source_media_type": source_media_type
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": "Failed to fetch similar titles"}), 500


@watched_bp.route("/watched/recommendations", methods=["POST"])
@login_required
def get_recommendations_from_watched():
    """Get recommendations based on random watched titles (movies and series)."""
    try:
        # Get recently watched movies and series
        movies = get_movies_watched(
            user_id=current_user.id,
            last_movie_id=None,
            last_date=None,
            limit=20
        ) or []
        
        series = get_series_watched(
            user_id=current_user.id,
            last_serie_id=None,
            last_date=None,
            limit=20
        ) or []
        
        # Combine into a unified list with media_type info
        all_watched = []
        for m in movies:
            all_watched.append({"id": m["api_movie_id"], "media_type": "movie"})
        for s in series:
            all_watched.append({"id": s["api_serie_id"], "media_type": "tv"})
        
        if not all_watched:
            return jsonify({"success": True, "results": []}), 200
        
        # Get IDs of titles user has already watched to exclude them
        watched_movie_ids = {m["api_movie_id"] for m in movies}
        watched_series_ids = {s["api_serie_id"] for s in series}
        
        # Pick up to 3 random titles to get recommendations from
        sample_size = min(3, len(all_watched))
        random_titles = random.sample(all_watched, sample_size)
        
        async def fetch_recommendations():
            async with aiohttp.ClientSession() as session:
                tasks = [
                    get_recommendations(session, t["id"], t["media_type"]) 
                    for t in random_titles
                ]
                results = await asyncio.gather(*tasks)
                return list(zip(random_titles, results))
        
        all_recommendations = asyncio.run(fetch_recommendations())
        
        # Combine and deduplicate results
        filtered_results = []
        seen_ids = set()
        
        for source_title, recs in all_recommendations:
            if not recs:
                continue
            media_type = source_title["media_type"]
            watched_ids = watched_movie_ids if media_type == "movie" else watched_series_ids
            
            for title in recs:
                title_id = title.get("id")
                # Create unique key combining id and media_type to avoid movie/tv id collision
                unique_key = f"{media_type}_{title_id}"
                
                if unique_key not in seen_ids and title_id not in watched_ids:
                    seen_ids.add(unique_key)
                    filtered_results.append(_filter_title_fields(title, media_type))
                    if len(filtered_results) >= 30:
                        break
            if len(filtered_results) >= 30:
                break
        
        return jsonify({
            "success": True,
            "results": filtered_results
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "message": "Failed to fetch recommendations"}), 500

