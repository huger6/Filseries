from flask import Blueprint, render_template
from flask_login import login_required

watched_bp = Blueprint("watched", __name__, template_folder="../templates/watched")

@watched_bp.route("/watched")
@login_required
def watched():
    return render_template("watched.html", page="watched")
