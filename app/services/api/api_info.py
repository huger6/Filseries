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


async def get_similar_titles(session, tmdb_id: int, media_type: str = "movie"):
    """Get similar titles from TMDB API.
    
    Args:
        session: aiohttp session
        tmdb_id: The TMDB ID of the title
        media_type: 'movie' or 'tv'
    """
    url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}/similar"
    params = {"api_key": api_key}
    
    async with session.get(url, params=params) as resp:
        if resp.status != 200:
            return None
        
        data = await resp.json()
        if not data.get("results"):
            return None
    
    return data["results"]


async def get_recommendations(session, tmdb_id: int, media_type: str = "movie"):
    """Get recommended titles from TMDB API based on a specific title.
    
    Args:
        session: aiohttp session
        tmdb_id: The TMDB ID of the title
        media_type: 'movie' or 'tv'
    """
    url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}/recommendations"
    params = {"api_key": api_key}
    
    async with session.get(url, params=params) as resp:
        if resp.status != 200:
            return None
        
        data = await resp.json()
        if not data.get("results"):
            return None
    
    return data["results"]


async def get_series_seasons_on_api(session, tmdb_id):
    """Get series seasons info from TMDB API"""
    url = f"https://api.themoviedb.org/3/tv/{tmdb_id}"
    params = {"api_key": api_key}

    async with session.get(url, params=params) as resp:
        if resp.status != 200:
            return None

        data = await resp.json()
        if not data:
            return None
        
        # Extract season info
        seasons = data.get("seasons", [])
        # Filter out "Specials" season (season_number = 0) and format the data
        formatted_seasons = []
        for season in seasons:
            season_number = season.get("season_number", 0)
            if season_number > 0:  # Skip specials (season 0)
                formatted_seasons.append({
                    "season_number": season_number,
                    "name": season.get("name", f"Season {season_number}"),
                    "episode_count": season.get("episode_count", 0),
                    "air_date": season.get("air_date"),
                    "poster_path": season.get("poster_path")
                })
        
        return {
            "number_of_seasons": data.get("number_of_seasons", 0),
            "seasons": formatted_seasons
        }


def __check_api_key():
    print(f"API KEY: {api_key}")