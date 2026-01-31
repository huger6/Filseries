from flask import Blueprint, flash, redirect, url_for, jsonify, render_template, request, get_flashed_messages, Response
from flask_login import login_required, current_user, login_user, logout_user
from app.validations import validateRegister, validateLogin
from app.exceptions import RegisterError, LoginError
from app.services.db_info import register_new_user, get_user_pfp, update_user_pfp

auth_bp = Blueprint("auth", __name__, template_folder='../templates/auth')


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == "POST":
        username = request.form.get("username")
        pw = request.form.get("password")

        try:
            user = validateLogin(username, pw)
            login_user(user) 
            return redirect(url_for('main.home'))
        except LoginError as e:
            get_flashed_messages() #clean buffer
            flash(f"{e}", "error")
            return render_template("login.html", page="login")

    return render_template("login.html", page="login")

@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    if current_user.get_id() == None:
        return redirect(url_for('main.home'))
    
    logout_user()

    get_flashed_messages() #clean buffer
    flash("You have been logged out. See you soon!", "success")
    return redirect(url_for('main.home'))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        pw = request.form.get("password")
        pw_confirm = request.form.get("confirm_password")
        
        try:
            if validateRegister(username, name, pw, pw_confirm):
                print("Validate register True")
                if register_new_user(username, name, pw):
                    return redirect(url_for('auth.login'))
                else:
                    raise RegisterError("An internal error has ocurred. Please try again later.")
        except RegisterError as e:
            return render_template("register.html", page="register", error=e)

    return render_template("register.html", page="register")

@auth_bp.route("/change-password")
def change_password():
    return render_template("changePassword.html", pages="change-password")

@auth_bp.route("/user")
@login_required
def user():
    has_pfp = get_user_pfp(current_user.id) is not None
    return render_template("user.html", page="user", has_pfp=has_pfp)

@auth_bp.route("/user/profile-picture", methods=["GET"])
@login_required
def get_profile_picture():
    """Return the user's profile picture as an image response"""
    pfp_data = get_user_pfp(current_user.id)
    if pfp_data:
        return Response(pfp_data, mimetype='image/jpeg')
    return jsonify({'error': 'No profile picture found'}), 404

@auth_bp.route("/user/profile-picture", methods=["POST"])
@login_required
def upload_profile_picture():
    """Upload a new profile picture"""
    if 'pfp' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['pfp']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check file type
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    file_ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if file_ext not in allowed_extensions:
        return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif, webp'}), 400
    
    # Read file data
    file_data = file.read()
    
    # Check file size (max 5MB)
    if len(file_data) > 5 * 1024 * 1024:
        return jsonify({'error': 'File size must be less than 5MB'}), 400
    
    # Update database
    if update_user_pfp(current_user.id, file_data):
        return jsonify({'success': True, 'message': 'Profile picture updated successfully'})
    
    return jsonify({'error': 'Failed to update profile picture'}), 500