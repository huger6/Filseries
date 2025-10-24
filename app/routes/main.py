from flask import Blueprint, render_template, flash
from flask_login import current_user

main_bp = Blueprint("main", __name__, template_folder="../templates/main")

@main_bp.route("/")
def home():
    return render_template("home.html", page="home")

@main_bp.route("/about")
def about():
    return render_template("about.html", page="about")

@main_bp.route("/privacy-policy")
def privacy():
    return render_template("privacy.html", page="privacy")