from flask import Blueprint, redirect, url_for, jsonify, render_template, request
from app.constants import app_constants
from app.exceptions import SearchError, RatingInvalid, TitleLengthInvalid, AcessDenied, StatusError 


error_handler_bp = Blueprint("error_handler", __name__, template_folder="../templates/error-handler")

# Error messages dictionary
ERROR_MESSAGES = {
    400: ("Bad Request", "The server could not understand your request. Please check and try again."),
    401: ("Unauthorized", "You need to be logged in to access this resource."),
    403: ("Forbidden", "You don't have permission to access this resource."),
    404: ("Page Not Found", "The page you're looking for doesn't exist or has been moved."),
    405: ("Method Not Allowed", "This action is not allowed on this resource."),
    408: ("Request Timeout", "The request took too long to process. Please try again."),
    429: ("Too Many Requests", "You've made too many requests. Please wait a moment and try again."),
    500: ("Internal Server Error", "Something went wrong on our end. Please try again later."),
    502: ("Bad Gateway", "We're having trouble connecting to the server. Please try again."),
    503: ("Service Unavailable", "The service is temporarily unavailable. Please try again later."),
    504: ("Gateway Timeout", "The server took too long to respond. Please try again."),
}


def render_error_page(error_code, custom_message=None):
    """Render a unified error page with the given error code and optional custom message."""
    title, default_message = ERROR_MESSAGES.get(error_code, ("Error", "An unexpected error occurred."))
    message = custom_message if custom_message else default_message
    
    # For API requests, return JSON
    if request.headers.get('Accept') == 'application/json' or request.is_json:
        return jsonify({'error': message}), error_code
    
    return render_template(
        "error.html",
        error_code=error_code,
        error_title=title,
        error_message=message,
        page='error'
    ), error_code


# HTTP Error Handlers

@error_handler_bp.app_errorhandler(400)
def handle_bad_request(e):
    return render_error_page(400)


@error_handler_bp.app_errorhandler(401)
def handle_unauthorized(e):
    return render_error_page(401)


@error_handler_bp.app_errorhandler(403)
def handle_forbidden(e):
    return render_error_page(403)


@error_handler_bp.app_errorhandler(404)
def handle_not_found(e):
    return render_error_page(404)


@error_handler_bp.app_errorhandler(405)
def handle_method_not_allowed(e):
    return render_error_page(405)


@error_handler_bp.app_errorhandler(500)
def handle_internal_error(e):
    return render_error_page(500)


@error_handler_bp.app_errorhandler(502)
def handle_bad_gateway(e):
    return render_error_page(502)


@error_handler_bp.app_errorhandler(503)
def handle_service_unavailable(e):
    return render_error_page(503)


# Custom Exception Handlers (User Errors - 400)

@error_handler_bp.errorhandler(SearchError)
def handle_search_error(e):
    return render_error_page(400, str(e))


@error_handler_bp.errorhandler(RatingInvalid)
def handle_rating_error(e):
    return render_error_page(400, str(e))


@error_handler_bp.errorhandler(StatusError)
def handle_status_error(e):
    return render_error_page(400, str(e))


@error_handler_bp.errorhandler(TitleLengthInvalid)
def handle_title_lenght_error(e):
    return render_error_page(400, str(e))


# Forbidden

@error_handler_bp.errorhandler(AcessDenied)
def handle_acess_denied(e):
    return render_error_page(403, str(e))


# Server Error (500)

@error_handler_bp.errorhandler(ValueError)
def handle_value_error(e):
    return render_error_page(500, str(e))
