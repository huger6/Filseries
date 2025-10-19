from dotenv import load_dotenv
import os
import aiohttp
import asyncio
from config import Config
from database import save_title_info

api_key = Config.API_KEY

async def get_title_info_on_api(session, tconst: str, titleType: str):
    if not tconst or not titleType:
        return {"tconst": tconst, "backdrop_path": "", "overview": "", "poster_path": ""}

    #Where to get the data
    if titleType in ["movie", "tvMovie"]:
        titleType = "movie_results"
    elif titleType in ["tvSeries", "tvMiniSeries"]:
        titleType = "tv_results"
    else:
        return {"tconst": tconst, "backdrop_path": "", "overview": "", "poster_path": ""}

    url = f"https://api.themoviedb.org/3/find/{tconst}?api_key={api_key}&external_source=imdb_id"

    try:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Erro na API para {tconst} - Status: {response.status}")
                return {"tconst": tconst, "backdrop_path": "", "overview": "", "poster_path": ""}

            data = await response.json()

            backdrop_path = ""
            overview = ""
            poster_path = ""

            if titleType in data and len(data[titleType]) > 0:
                result = data[titleType][0]

                return {"tconst": tconst, **result}
            return {"tconst": tconst, "backdrop_path": "", "overview": "", "poster_path": ""}

    except Exception as e:
        print(f"Erro ao procurar {tconst} na API: {e}")
        return {"tconst": tconst, "backdrop_path": "", "overview": "", "poster_path": ""}


async def get_multiple_titles_info(titles):
    async with aiohttp.ClientSession() as session:
        tasks = [get_title_info_on_api(session, title["tconst"], title["titleType"]) for title in titles]
        return await asyncio.gather(*tasks)

async def search_title_and_get_tconst(session, query: str, title_type: str):
    base = "https://api.themoviedb.org/3"
    search_type = "movie" if title_type == "movie" else "tv"

    search_url = f"{base}/search/{search_type}?api_key={api_key}&query={query}"

    async with session.get(search_url) as resp:
        data = await resp.json()
        if not data["results"]:
            return None  # não encontrou nada

        # pegar o primeiro resultado
        result = data["results"][0]
        tmdb_id = result["id"]

    # agora buscar o imdb_id
    external_url = f"{base}/{search_type}/{tmdb_id}/external_ids?api_key={api_key}"

    async with session.get(external_url) as resp:
        ids_data = await resp.json()
        imdb_id = ids_data.get("imdb_id")

    return {"tmdb_id": tmdb_id, "imdb_id": imdb_id, "data": result}


def getTitleInfo(apiResult):
    if apiResult:
        return {
            "poster_path": apiResult["poster_path"] or "",
            "backdrop_path": apiResult["backdrop_path"] or "",
            "overview": apiResult["overview"] or "",
        }
    #Trocar depois de testar
    return {
        "poster_path": "", 
        "backdrop_path": "", 
        "overview": ""
    }


def __check_api_key():
    print(f"API KEY: {api_key}")