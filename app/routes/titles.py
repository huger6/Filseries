from flask import Blueprint, flash, redirect, url_for, jsonify, render_template, request, get_flashed_messages
from flask_login import login_required, current_user
import asyncio
# Database
from app.models.user import db
# Constants
from app.constants import LIMIT_PER_PAGE, SORT_BY_FILTERS, SORT_BY_ORDERS
from app.constants import GENRES_DEFAULT
# Validations
from app.validations import validate_title, validate_page, validate_limit_per_page
from app.validations import validate_sort_by, validate_genres, validate_years, validate_ratings
# API
from app.services.api_info import search_title_on_api

titles_bp = Blueprint("titles", __name__, template_folder="../templates/titles")

@titles_bp.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        titleType = request.args.getlist("titleTypes")
        if not titleType:
            titleType = ""

        # Validations
        try:
            # Title
            title = request.args.get("title")
            validate_title(title)
            # Page
            page = int(request.args.get("page", 1))
            validate_page(page)
            # Limits
            limit = int(request.args.get("limit", LIMIT_PER_PAGE))
            validate_limit_per_page(limit)
            # Sort By
            sort_by = [request.args.get("filter", SORT_BY_FILTERS[0]), request.args.get("order", SORT_BY_ORDERS[0])]
            validate_sort_by((sort_by[0], sort_by[1]))
            # Genres
            genres = request.args.getlist("genres")
            if not genres:
                genres = GENRES_DEFAULT
            else:
                genres = validate_genres(genres)
            # Years
            try:
                years = tuple(int(year) for year in request.args.getlist("years"))
            except ValueError:
                raise ValueError("Years type are invalid")
            validate_years(years)
            # Ratings
            try:
                ratings = tuple(float(rat) for rat in request.args.getlist("ratings"))
            except ValueError:
                raise ValueError("Rating type is invalid")
            validate_ratings(ratings)
        except Exception as e:
            get_flashed_messages()
            flash(str(e), 'error')
            return render_template("search.html", page="search")

        data = asyncio.run(search_title_on_api(query=title, title_type=titleType))
        print(data)

        return render_template("search.html", results=data["results"], query=title, page="search")
    
@titles_bp.route("/title/<string:media_type>/<int:id>", methods=["GET"])
def title(media_type, id):
    if request.method == "GET":
        return render_template("title.html", title="Title not found", results=None)

        user_id = current_user.get_id() if current_user.is_authenticated else None
        # results = getTitleInformationDetailed(tconst, user_id)
        # print(f"{results}!")
        # if results:
        #     return render_template("title.html", title=results[0]["primaryTitle"], results=results)
    return render_template("title.html", title="Title not found", results=None)
    