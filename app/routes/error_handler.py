from flask import Blueprint, redirect, url_for, jsonify, render_template


error_handler_bp = Blueprint("error_handler_bp", __name__, template_folder="../templates/error-handler")

#User Error (400)

@error_handler_bp.errorhandler(SearchError)
def handle_rating_error(e):
    return jsonify({'error': str(e)}), 400

@error_handler_bp.errorhandler(RatingInvalid)
def handle_rating_error(e):
    return jsonify({'error': str(e)}), 400

@error_handler_bp.errorhandler(StatusError)
def handle_status_error(e):
    return jsonify({'error': str(e)}), 400

@error_handler_bp.errorhandler(TitleLenghtInvalid)
def handle_title_lenght_error(e):
    return jsonify({'error': str(e)}), 400

#Forbidden

@error_handler_bp.errorhandler(AcessDenied)
def handle_acess_denied(e):
    return jsonify({'error': str(e)}), 403


#Server Error (500)

@error_handler_bp.errorhandler(ValueError)
def handle_ValueError(e):
    return jsonify({'error': str(e)}), 500

@error_handler_bp.errorhandler(Error) #From sqlite3
def handle_db_error(e):
    return jsonify({'error': str(e)}), 500
