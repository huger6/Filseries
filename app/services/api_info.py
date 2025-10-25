from dotenv import load_dotenv
import aiohttp
import asyncio
from config import Config

api_key = Config.API_KEY


async def search_title_on_api(session, query: str, title_type: str = None):
    """Search title in api. Only returns data["results"]"""
    base = "https://api.themoviedb.org/3"
    if title_type in ("movie", "tv"):
        search_type = title_type
    else:
        search_type = "multi"

    url = f"{base}/search/{search_type}"
    params = {"api_key": api_key, "query": query, "include_adult": "false"}


    async with session.get(url, params=params) as resp:
        if resp.status != 200:
            return None

        data = await resp.json()
        if not data["results"]:
            return None

    return data["results"]

async def get_title_tconst_on_api(session, tmdb_id, search_type):
    """Get title tconst from TMDB API"""
    url = f"https://api.themoviedb.org/3/{search_type}/{tmdb_id}/external_ids"
    params = {"api_key": api_key}

    async with session.get(url, params=params) as resp:
        ids_data = await resp.json()
        imdb_id = ids_data.get("imdb_id")

    return imdb_id

async def get_title_info_on_api(session, tmdb_id, search_type):
    """Get title info from TMDB API"""
    url = f"https://api.themoviedb.org/3/{search_type}/{tmdb_id}"
    params = {"api_key": api_key}

    async with session.get(url, params=params) as resp:
        if resp.status != 200:
            return None

        data = await resp.json()
        if not data["results"]:
            return None
        
        return data["results"]

def __check_api_key():
    print(f"API KEY: {api_key}")