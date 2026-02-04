from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.services.db import (
    create_notification,
    delete_notification,
    mark_notification_as_read,
    get_user_notifications,
    get_unread_notification_count,
)

notifications_bp = Blueprint("notifications", __name__, template_folder="../templates/notifications")

@notifications_bp.route("/notifications/unread", methods=["GET"])
@login_required
def get_unread_notifications():
    pass

@notifications_bp.route("/notifications/all", methods=["GET"])
@login_required
def get_all_notifications():
    pass

@notifications_bp.route("/notifications/mark-as-read", methods=["POST"])
@login_required
def mark_notification_as_read():
    pass

@notifications_bp.route("/notifications/mark-as-read/all", methods=["POST"])
@login_required
def mark_all_notifications_as_read():
    pass

@notifications_bp.route("/notifications/delete", methods=["POST"])
@login_required
def delete_notification():
    pass

@notifications_bp.route("/notifications/delete/all", methods=["POST"])
@login_required
def delete_all_notifications():
    pass
