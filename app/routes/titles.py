from flask import Blueprint, flash, redirect, url_for, render_template, request, get_flashed_messages
from flask_login import current_user
import asyncio
# Validations
from app.validations import validate_title
# API
from app.services.search_info import search_title, get_title_info

titles_bp = Blueprint("titles", __name__, template_folder="../templates/titles")

@titles_bp.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        title = request.args.get("title", "").strip()
        
        # If no search term provided, redirect to home
        if not title:
            return redirect(url_for('main.home'))
        
        titleType = request.args.getlist("titleTypes")
        if not titleType:
            titleType = ""

        # Validations
        try:
            validate_title(title)
        except Exception as e:
            # Return to home with user-friendly message for title validation errors
            get_flashed_messages()
            flash(str(e), 'error')
            return redirect(url_for('main.home'))

        # Get user ID
        user_id = current_user.get_id() if current_user.is_authenticated else None
        
        # Get results
        try:
            data = asyncio.run(search_title(query=title, search_type=titleType, user_id=user_id))
        except Exception:
            # Handle API errors gracefully
            data = []

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
    