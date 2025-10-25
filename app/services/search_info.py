import asyncio
import aiohttp
from app.services.api_info import search_title_on_api, get_title_info_on_api, get_title_tconst_on_api
from app.services.db_info import fetch_user_marks_id, fetch_user_marks
# Constants
from app.constants import ALLOWED_FIELDS_SEARCH


async def search_title(query: str, search_type: str, user_id):
    """Search title from TMDB API"""
    async with aiohttp.ClientSession() as session:
        data = await search_title_on_api(session, query, search_type)
        # Filter data 
        filtered_data = [_filter_fields(i, ALLOWED_FIELDS_SEARCH) for i in data if i.get("title")]
        # Get IDs
        tmdb_ids = [int(r["id"]) for r in filtered_data if "id" in r]
        # Get titles-user information
        user_marks = fetch_user_marks_id(user_id, tmdb_ids)
        titles_seen = user_marks["movies_seen"] | user_marks["series_seen"]
        titles_watchlist = user_marks["movies_watchlist"] | user_marks["series_watchlist"]
        # Group information
        for entry in filtered_data:
            entry_id = entry["id"]
            entry["seen"] = entry_id in titles_seen
            entry["in_watchlist"] = entry_id in titles_watchlist
            entry["release_date"] = str(_format_date(entry["release_date"])) # Format date

        return filtered_data
    
async def get_title_info(id: int, search_type: str, user_id = None):
    """Get a title's information from the database"""
    async with aiohttp.ClientSession() as session:
        data = await get_title_info_on_api(session, id, search_type)
        # Get tconst
        tconst = await get_title_tconst_on_api(session, id, search_type)
        # Get user info
        user_marks = fetch_user_marks(user_id, id, search_type)
        # Group all info
        for entry in data:
            entry["tconst"] = tconst if tconst else None
            entry["seen"] = user_marks["seen"] # List of dicts
            entry["watchlist"] = user_marks["watchlist"] # bool

    return data if data else None


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