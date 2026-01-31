import aiohttp
from app.services.api.api_info import (
    search_title_on_api, 
    get_title_info_on_api, 
    get_title_tconst_on_api,
    get_trending_titles,
    get_popular_titles,
    get_top_rated_titles
)
from app.services.db.db_info import fetch_user_marks_id, fetch_user_marks
# Constants
from app.constants import ALLOWED_FIELDS_SEARCH, ALLOWED_FIELDS_TITLE_SEARCH


async def get_home_page_data():
    """Get data for the home page including trending, popular movies/TV and top rated."""
    async with aiohttp.ClientSession() as session:
        # Fetch all data
        trending = await get_trending_titles(session, "all", "week")
        popular_movies = await get_popular_titles(session, "movie")
        popular_tv = await get_popular_titles(session, "tv")
        top_rated_movies = await get_top_rated_titles(session, "movie")
        top_rated_tv = await get_top_rated_titles(session, "tv")
        
        # Process and filter the data
        def process_results(data, media_type=None):
            if not data:
                return []
            processed = []
            for item in data[:20]:  # Limit to 20 items per section
                entry = _filter_fields(item, ALLOWED_FIELDS_SEARCH)
                # Get the title (movies use 'title', TV uses 'name')
                title = item.get("title") or item.get("name")
                if not title:
                    continue
                entry["title"] = title
                # Get release date
                date_val = item.get("release_date") or item.get("first_air_date")
                entry["release_date"] = _format_date(date_val)
                # Set media type
                entry["media_type"] = media_type or item.get("media_type", "movie")
                processed.append(entry)
            return processed
        
        return {
            "trending": process_results(trending),
            "popular_movies": process_results(popular_movies, "movie"),
            "popular_tv": process_results(popular_tv, "tv"),
            "top_rated_movies": process_results(top_rated_movies, "movie"),
            "top_rated_tv": process_results(top_rated_tv, "tv")
        }


async def search_title(query: str, search_type: str, user_id):
    """Search title from TMDB API"""
    async with aiohttp.ClientSession() as session:
        data = await search_title_on_api(session, query, search_type)
        # Handle None or empty response
        if not data:
            return []
        # Filter data - only include movie and tv media types
        filtered_data = []
        for i in data:
            # Skip if no title/name
            if not (i.get("title") or i.get("name")):
                continue
            # Only include movie and tv media types
            media_type = i.get("media_type")
            if search_type in ("movie", "tv"):
                # If searching by specific type, use that type
                media_type = search_type
            elif media_type not in ("movie", "tv"):
                # Skip person and other types in multi search
                continue
            
            entry = _filter_fields(i, ALLOWED_FIELDS_SEARCH)
            entry["media_type"] = media_type
            filtered_data.append(entry)
        
        # Get IDs
        tmdb_ids = [int(r["id"]) for r in filtered_data if "id" in r]
        # Get titles-user information
        user_marks = fetch_user_marks_id(user_id, tmdb_ids)
        titles_seen = user_marks["movies_seen"] | user_marks["series_seen"]
        titles_watchlist = user_marks["movies_watchlist"] | user_marks["series_watchlist"]
        # Group information
        for entry in filtered_data:
            entry_id = entry.get("id")
            entry["seen"] = entry_id in titles_seen if entry_id is not None else False
            entry["in_watchlist"] = entry_id in titles_watchlist if entry_id is not None else False
            # TMDB uses release_date for movies and first_air_date for TV shows
            date_val = entry.get("release_date") or entry.get("first_air_date")
            entry["release_date"] = _format_date(date_val)  # Format date
            # Change series name to title 
            title = entry.get("name")
            if title:
                entry["title"] = entry.pop("name")

        return filtered_data
    
async def get_title_info(id: int, search_type: str, user_id = None) -> dict:
    """Get a title's information from the database"""
    async with aiohttp.ClientSession() as session:
        data = await get_title_info_on_api(session, id, search_type)
        # Get tconst
        tconst = await get_title_tconst_on_api(session, id, search_type)
        # Get user info
        user_marks = fetch_user_marks(user_id, id, search_type)
        # Filter information
        data = _filter_fields(data, ALLOWED_FIELDS_TITLE_SEARCH)
        # Group all info
        if data:
            data["tconst"] = tconst if tconst else None
            data["seen"] = user_marks["seen"] # List of dicts
            data["watchlist"] = user_marks["watchlist"] # bool
            data["media_type"] = search_type
            # Normalize TV series name to title (TMDB uses 'name' for TV, 'title' for movies)
            if "name" in data and "title" not in data:
                data["title"] = data.pop("name")
            # Handle first_air_date for TV shows
            if "first_air_date" in data and "release_date" not in data:
                data["release_date"] = data.get("first_air_date")

    return data if data else {}


def _filter_fields(item: dict, allowed_fields):
    return {k: v for k, v in item.items() if k in allowed_fields}

def _format_date(release_date: str):
    if not release_date or not str(release_date).strip():
        return None
    
    try:
        year = release_date.split(sep="-")[0]
    except Exception:
        return None
    return year
