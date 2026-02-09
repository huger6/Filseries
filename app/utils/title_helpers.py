import asyncio
import random
from datetime import datetime

import aiohttp
from flask import jsonify, request
from flask_login import current_user

from app.constants import ALLOWED_FIELDS_SEARCH
from app.exceptions import StatusError
from app.services.api.api_info import get_recommendations, get_similar_titles
from app.services.search_info import fetch_titles_info_batch
from app.validations import validate_pagination_params


def merge_user_data(title_entry: dict, user_data: dict) -> dict:
    """Merge user-specific data (rating, status, etc.) into title entry."""
    if not user_data:
        return title_entry

    result = title_entry.copy()

    if "user_rating" in user_data:
        result["user_rating"] = user_data["user_rating"]
    if "updated_at" in user_data:
        result["updated_at"] = (
            user_data["updated_at"].isoformat()
            if isinstance(user_data["updated_at"], datetime)
            else user_data["updated_at"]
        )
    if "last_season_seen" in user_data:
        result["last_season_seen"] = user_data["last_season_seen"]
    if "status" in user_data:
        result["status"] = user_data["status"]

    return result


def filter_title_fields(title: dict, media_type: str) -> dict:
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


def get_paginated_titles(db_fetch_fn, media_type: str, id_field: str, error_msg: str):
    """
    Generic handler for paginated title endpoints (movies/series for watched/watchlist).

    Args:
        db_fetch_fn: Function to call to get DB results. Signature:
                     (user_id, last_<type>_id, last_date, limit) -> list[dict]
        media_type: 'movie' or 'tv'
        id_field: The key in db results for the API ID (e.g. 'api_movie_id' or 'api_serie_id')
        error_msg: Error message to return on failure
    """
    data = request.get_json() or {}

    try:
        last_id, last_date, limit = validate_pagination_params(
            data.get("last_id"),
            data.get("last_date"),
            data.get("limit"),
        )
    except StatusError as e:
        return jsonify({"success": False, "message": str(e)}), 400

    try:
        # Build kwargs dynamically based on media type
        id_param = "last_movie_id" if media_type == "movie" else "last_serie_id"
        db_results = db_fetch_fn(
            user_id=current_user.id,
            **{id_param: last_id},
            last_date=last_date,
            limit=limit,
        )

        if not db_results:
            return jsonify({"success": True, "results": [], "has_more": False}), 200

        # Extract IDs and user data
        title_ids = [r[id_field] for r in db_results]
        user_data_map = {r[id_field]: r for r in db_results}

        # Fetch title info from TMDB API
        title_info_map = asyncio.run(fetch_titles_info_batch(title_ids, media_type))

        # Process and combine results
        results = []
        for title_id in title_ids:
            title_data = title_info_map.get(title_id)
            if title_data:
                processed = merge_user_data(title_data, user_data_map.get(title_id))
                results.append(processed)

        has_more = len(db_results) >= limit

        return jsonify({"success": True, "results": results, "has_more": has_more}), 200

    except Exception:
        return jsonify({"success": False, "message": error_msg}), 500


def get_similar_titles_for_user(get_movies_fn, get_series_fn, error_msg: str):
    """
    Generic handler for fetching similar titles based on a user's titles.

    Args:
        get_movies_fn: DB function to get user's movies
        get_series_fn: DB function to get user's series
        error_msg: Error message to return on failure
    """
    try:
        movies = (
            get_movies_fn(
                user_id=current_user.id,
                last_movie_id=None,
                last_date=None,
                limit=15,
            )
            or []
        )

        series = (
            get_series_fn(
                user_id=current_user.id,
                last_serie_id=None,
                last_date=None,
                limit=15,
            )
            or []
        )

        # Combine into a unified list with media_type info
        all_titles = []
        for m in movies:
            all_titles.append({"id": m["api_movie_id"], "media_type": "movie"})
        for s in series:
            all_titles.append({"id": s["api_serie_id"], "media_type": "tv"})

        if not all_titles:
            return jsonify({"success": True, "results": []}), 200

        # Get IDs to exclude
        movie_ids_set = {m["api_movie_id"] for m in movies}
        series_ids_set = {s["api_serie_id"] for s in series}

        # Pick a random title
        random_title = random.choice(all_titles)
        source_id = random_title["id"]
        source_media_type = random_title["media_type"]

        async def fetch_similar():
            async with aiohttp.ClientSession() as session:
                results = await get_similar_titles(session, source_id, source_media_type)
                return results or []

        similar_titles = asyncio.run(fetch_similar())

        exclude_ids = movie_ids_set if source_media_type == "movie" else series_ids_set

        filtered_results = []
        seen_ids = set()

        for title in similar_titles:
            title_id = title.get("id")
            if title_id not in seen_ids and title_id not in exclude_ids:
                seen_ids.add(title_id)
                filtered_results.append(filter_title_fields(title, source_media_type))
                if len(filtered_results) >= 30:
                    break

        return (
            jsonify(
                {
                    "success": True,
                    "results": filtered_results,
                    "source_id": source_id,
                    "source_media_type": source_media_type,
                }
            ),
            200,
        )

    except Exception:
        return jsonify({"success": False, "message": error_msg}), 500


def get_recommendations_for_user(get_movies_fn, get_series_fn, error_msg: str):
    """
    Generic handler for fetching recommendations based on a user's titles.

    Args:
        get_movies_fn: DB function to get user's movies
        get_series_fn: DB function to get user's series
        error_msg: Error message to return on failure
    """
    try:
        movies = (
            get_movies_fn(
                user_id=current_user.id,
                last_movie_id=None,
                last_date=None,
                limit=20,
            )
            or []
        )

        series = (
            get_series_fn(
                user_id=current_user.id,
                last_serie_id=None,
                last_date=None,
                limit=20,
            )
            or []
        )

        all_titles = []
        for m in movies:
            all_titles.append({"id": m["api_movie_id"], "media_type": "movie"})
        for s in series:
            all_titles.append({"id": s["api_serie_id"], "media_type": "tv"})

        if not all_titles:
            return jsonify({"success": True, "results": []}), 200

        movie_ids_set = {m["api_movie_id"] for m in movies}
        series_ids_set = {s["api_serie_id"] for s in series}

        sample_size = min(3, len(all_titles))
        random_titles = random.sample(all_titles, sample_size)

        async def fetch_recs():
            async with aiohttp.ClientSession() as session:
                tasks = [
                    get_recommendations(session, t["id"], t["media_type"])
                    for t in random_titles
                ]
                results = await asyncio.gather(*tasks)
                return list(zip(random_titles, results))

        all_recommendations = asyncio.run(fetch_recs())

        filtered_results = []
        seen_ids = set()

        for source_title, recs in all_recommendations:
            if not recs:
                continue
            media_type = source_title["media_type"]
            exclude_ids = movie_ids_set if media_type == "movie" else series_ids_set

            for title in recs:
                title_id = title.get("id")
                unique_key = f"{media_type}_{title_id}"

                if unique_key not in seen_ids and title_id not in exclude_ids:
                    seen_ids.add(unique_key)
                    filtered_results.append(filter_title_fields(title, media_type))
                    if len(filtered_results) >= 30:
                        break
            if len(filtered_results) >= 30:
                break

        return jsonify({"success": True, "results": filtered_results}), 200

    except Exception:
        return jsonify({"success": False, "message": error_msg}), 500
