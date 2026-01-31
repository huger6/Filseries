from flask import Blueprint, flash, redirect, url_for, jsonify, render_template, request, get_flashed_messages
from flask_login import login_required, current_user
import asyncio
# Constants
from app.constants import LIMIT_PER_PAGE, SORT_BY_FILTERS, SORT_BY_ORDERS
from app.constants import GENRES_DEFAULT
# Validations
from app.validations import validate_title, validate_page, validate_limit_per_page
from app.validations import validate_sort_by, validate_genres, validate_years, validate_ratings
# API
from app.services.api.search_info import search_title, get_title_info

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

        # Get user ID
        user_id = current_user.get_id() if current_user.is_authenticated else None
        # Get results
        data = asyncio.run(search_title(query=title, search_type=titleType, user_id=user_id))

        return render_template("search.html", results=data, query=title, page="search")
    
@titles_bp.route("/title/<media:media_type>/<int:id>", methods=["GET"])
def title(media_type, id):
    if request.method == "GET":
        # Get user ID
        user_id = current_user.get_id() if current_user.is_authenticated else None
        # Get results
        data = asyncio.run(get_title_info(id=id, search_type=media_type, user_id=user_id))
        if data:
            return render_template("title.html", primaryTitle=data["title"], results=data)
    return render_template("title.html", primaryTitle="Title not found", results=None)
    