from flask import Blueprint, render_template, flash
from flask_login import current_user
import asyncio
from app.services.search_info import get_home_page_data

main_bp = Blueprint("main", __name__, template_folder="../templates/main")

@main_bp.route("/")
def home():
    # Get home page data (trending, popular, top rated)
    home_data = asyncio.run(get_home_page_data())
    return render_template("home.html", page="home", **home_data)

@main_bp.route("/about")
def about():
    return render_template("about.html", page="about")

@main_bp.route("/privacy-policy")
def privacy():
    return render_template("privacy.html", page="privacy")