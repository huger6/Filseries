from flask import Blueprint, flash, redirect, url_for, jsonify, render_template, request, get_flashed_messages
from flask_login import login_required, current_user
from app.models.user import db
from app.constants import LIMIT_PER_PAGE, SORT_BY_FILTERS, SORT_BY_ORDERS
from app.constants import GENRES_DEFAULT, TITLE_TYPE_DEFAULT
from app.validations import validate_title_length, validate_page, validate_limit_per_page
from app.validations import validate_sort_by, validate_genres, validate_years, validate_ratings

titles_bp = Blueprint("titles", __name__, template_folder="../templates/titles")

@titles_bp.route("/search", methods=["GET", "POST"])
def search():
    start_time = time.perf_counter()

    if request.method == "GET":
        title = request.args.get("title")
        if not title:
            raise SearchError("Title cannot be null")
        
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", LIMIT_PER_PAGE))

        sort_by = [request.args.get("filter", SORT_BY_FILTERS[0]), request.args.get("order", SORT_BY_ORDERS[0])]

        genres = request.args.getlist("genres")
        if not genres:
            genres = GENRES_DEFAULT

        try:
            years = tuple(int(year) for year in request.args.getlist("years"))
        except ValueError:
            raise ValueError("Year is not of type int")
        
        try:
            ratings = tuple(float(rat) for rat in request.args.getlist("ratings"))
        except ValueError:
            raise ValueError("Rating is not of type float")
        
        titleType = request.args.getlist("titleTypes")
        if not titleType:
            titleType = TITLE_TYPE_DEFAULT

        # Validations
        try:
            validate_title_length(title)
            validate_page(page)
            validate_limit_per_page(limit)
            validate_sort_by(sort_by[0], sort_by[1])
            validate_genres(genres)
            validate_years(years)
            validate_ratings(ratings)
        except Exception as e:
            get_flashed_messages()
            flash(str(e), 'error')
            return render_template("search.html", page="search")

        data = search_db(current_user.get_id() if current_user.is_authenticated else None,
                    title, page, limit, sort_by, genres, years, ratings, titleType)

        mid_time = time.perf_counter()
        print(f"Tempo para retornar dados: {mid_time - start_time:.2f}")

        needInfo = []
        for title in data:
            #Check if title's info isn't in the db
            if title["poster_path"] is None:
                needInfo.append({"tconst": title["tconst"], "titleType": title["titleType"]})
        
        if needInfo:
            apiResults = asyncio.run(get_multiple_titles_info(needInfo))

            for title, apiResult in zip(data, apiResults):
                if title["tconst"] in [entry["tconst"] for entry in needInfo]:
                    title.update(getTitleInfo(apiResult))

        end_time = time.perf_counter()
        print(f"Procurar dados: {end_time - mid_time:.2f}")
        return render_template("search.html", results=data)
    
# @titles_bp.route("/title", methods=["GET"])
# def title():
#     if request.method == "GET":
#         tconst = request.args.get("id")
#         if not tconst:
#             return render_template("title.html", title="Title not found", results=None)

#         user_id = current_user.get_id() if current_user.is_authenticated else None
#         results = getTitleInformationDetailed(tconst, user_id)
#         print(f"{results}!")
#         if results:
#             return render_template("title.html", title=results[0]["primaryTitle"], results=results)
#     return render_template("title.html", title="Title not found", results=None)
    

@titles_bp.route("/search", methods=["GET", "POST"])
def search():
    return render_template("search.html", page="search")