from flask import Blueprint, flash, redirect, url_for, jsonify, render_template, request
from flask_login import login_required, current_user
from app.models.models import bcrypt, db, User

watchlist_bp = Blueprint("watchlist_bp", __name__, template_folder="../templates/watchlist")

