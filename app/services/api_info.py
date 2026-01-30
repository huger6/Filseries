from dotenv import load_dotenv
from config import Config

api_key = Config.API_KEY


async def get_trending_titles(session, media_type: str = "all", time_window: str = "week"):
    """Get trending titles from TMDB API.
    
    Args:
        session: aiohttp session
        media_type: 'all', 'movie', or 'tv'
        time_window: 'day' or 'week'
    """
    url = f"https://api.themoviedb.org/3/trending/{media_type}/{time_window}"
    params = {"api_key": api_key}
    
    async with session.get(url, params=params) as resp:
        if resp.status != 200:
            return None
        
        data = await resp.json()
        if not data.get("results"):
            return None
    
    return data["results"]


async def get_popular_titles(session, media_type: str = "movie"):
    """Get popular titles from TMDB API.
    
    Args:
        session: aiohttp session
        media_type: 'movie' or 'tv'
    """
    url = f"https://api.themoviedb.org/3/{media_type}/popular"
    params = {"api_key": api_key}
    
    async with session.get(url, params=params) as resp:
        if resp.status != 200:
            return None
        
        data = await resp.json()
        if not data.get("results"):
            return None
    
    return data["results"]


async def get_top_rated_titles(session, media_type: str = "movie"):
    """Get top rated titles from TMDB API.
    
    Args:
        session: aiohttp session
        media_type: 'movie' or 'tv'
    """
    url = f"https://api.themoviedb.org/3/{media_type}/top_rated"
    params = {"api_key": api_key}
    
    async with session.get(url, params=params) as resp:
        if resp.status != 200:
            return None
        
        data = await resp.json()
        if not data.get("results"):
            return None
    
    return data["results"]


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

        data = await resp.json() # Returns a dict
        
        return data if data else None


def __check_api_key():
    print(f"API KEY: {api_key}")