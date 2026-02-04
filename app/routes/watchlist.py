from flask import Blueprint, flash, redirect, url_for, jsonify, render_template, request
from flask_login import login_required

watchlist_bp = Blueprint("watchlist", __name__, template_folder="../templates/watchlist")

@watchlist_bp.route("/watchlist")
@login_required
def watchlist():
    return render_template("watchlist.html", page="watchlist")

