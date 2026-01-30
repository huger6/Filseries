from flask import Blueprint, flash, redirect, url_for, jsonify, render_template, request
from flask_login import login_required

watchlist_bp = Blueprint("watchlist", __name__, template_folder="../templates/watchlist")

@watchlist_bp.route("/watchlist")
@login_required
def watchlist():
    return render_template("watchlist.html", page="watchlist")

# @watchlist_bp.route("/watchlist/add/<int:id>", methods=["GET"])
# @login_required
# def add_to_watchlist(id: int):
#     # Check if id is valid
    

#     # Add title to the user's watchlist

#     return jsonify({'sucess': True})
#     return jsonify({'sucess': False})

# @watchlist_bp.route("watchlist/remove/<int:id>", methods=["GET"])
# @login_required
# def remove_from_watchlist(id: int):
#     # Check if the id is valid

#     # Check if the id exists in the watchlist

#     # If it exists remove from watchlist

#     return jsonify({'sucess': True})
#     return jsonify({'sucess': False})