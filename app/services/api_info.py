from dotenv import load_dotenv
import aiohttp
import asyncio
from config import Config

api_key = Config.API_KEY


async def search_title_on_api(query: str, title_type: str):
    """Search title in api"""
    async with aiohttp.ClientSession() as session:
        data = await __search_title_on_api(session, query, title_type)
        return data

async def __search_title_on_api(session, query: str, title_type: str = None):
    """Search title in api"""
    base = "https://api.themoviedb.org/3"
    if title_type in ("movie", "tv"):
        search_type = title_type
    else:
        search_type = "multi"

    search_url = f"{base}/search/{search_type}"
    params = {"api_key": api_key, "query": query}


    async with session.get(search_url, params=params) as resp:
        if resp.status != 200:
            return None

        data = await resp.json()
        if not data["results"]:
            return None

    return data

async def get_title_tconst_on_api(session, tmdb_id, search_type):
    """Get title tconst"""
    url = f"https://api.themoviedb.org/3/{search_type}/{tmdb_id}/external_ids?api_key={api_key}"

    async with session.get(url) as resp:
        ids_data = await resp.json()
        imdb_id = ids_data.get("imdb_id")

    return imdb_id

def __check_api_key():
    print(f"API KEY: {api_key}")