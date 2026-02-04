from flask import Blueprint, flash, redirect, url_for, jsonify, render_template, request, get_flashed_messages, Response
from flask_login import login_required, current_user, login_user, logout_user
from app.validations import validateRegister, validateLogin, validateUsername, validatePassword, validatePasswordConfirm
from app.exceptions import RegisterError, LoginError, AuthError
from app.services.db import register_new_user, get_user_pfp, update_user_pfp, username_available, change_user_username as db_change_username, change_user_password
from app.utils.valid_next_page import enpoint_is_valid, is_safe_url
from app.extensions import bcrypt

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
            
            # Redirect to next page if provided, otherwise home
            next_page = request.args.get('next')
            if next_page:
                # First check if it's a valid endpoint name
                if enpoint_is_valid(next_page):
                    return redirect(url_for(next_page))
                # Then check if it's a safe relative URL
                elif is_safe_url(next_page):
                    return redirect(next_page)
            return redirect(url_for('main.home'))
        except LoginError as e:
            get_flashed_messages() # clean buffer
            flash(f"{e}", "error")
            return render_template("login.html", page="login")

    return render_template("login.html", page="login")

@auth_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    if current_user.get_id() == None:
        return redirect(url_for('main.home'))
    
    logout_user()

    get_flashed_messages() # clean buffer
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
                if register_new_user(username, name, pw):
                    return redirect(url_for('auth.login'))
                else:
                    raise RegisterError("An internal error has ocurred. Please try again later.")
        except RegisterError as e:
            return render_template("register.html", page="register", error=e)

    return render_template("register.html", page="register")

@auth_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    """Handle password change"""
    if request.method == "POST":
        current_pw = request.form.get("current_password")
        new_pw = request.form.get("new_password")
        confirm_pw = request.form.get("confirm_password")
        
        # Validate current password
        if not bcrypt.check_password_hash(current_user.pass_hash, current_pw):
            return jsonify({'success': False, 'error': 'Current password is incorrect'}), 400
        
        # Validate new password format
        if not validatePassword(new_pw):
            return jsonify({'success': False, 'error': 'New password does not meet requirements'}), 400
        
        # Validate passwords match
        if not validatePasswordConfirm(new_pw, confirm_pw):
            return jsonify({'success': False, 'error': 'Passwords do not match'}), 400
        
        # Update password
        if change_user_password(current_user.id, new_pw):
            return jsonify({'success': True, 'message': 'Password updated successfully'})
        
        return jsonify({'success': False, 'error': 'Failed to update password'}), 500
    
    return render_template("changePassword.html", page="change-password")

@auth_bp.route("/user/check-username", methods=["POST"])
@login_required
def check_username_availability():
    """Check if a username is available via AJAX"""
    data = request.get_json()
    new_username = data.get('username', '').strip()
    
    # If same as current username, it's available (for them)
    if new_username.lower() == current_user.username.lower():
        return jsonify({'available': True, 'message': 'This is your current username'})
    
    # Validate username format
    if not validateUsername(new_username):
        return jsonify({'available': False, 'message': 'Invalid username format (3-12 chars, letters, numbers, _ and . only)'})
    
    # Check availability
    if username_available(new_username):
        return jsonify({'available': True, 'message': 'Username is available'})
    
    return jsonify({'available': False, 'message': 'Username is already taken'})

@auth_bp.route("/user/username", methods=["POST"])
@login_required
def update_username():
    """Update the user's username"""
    data = request.get_json()
    new_username = data.get('username', '').strip()
    
    # Validate username format
    if not validateUsername(new_username):
        return jsonify({'success': False, 'error': 'Invalid username format'}), 400
    
    # Check if same as current
    if new_username == current_user.username:
        return jsonify({'success': False, 'error': 'This is already your username'}), 400
    
    # Check availability
    if not username_available(new_username):
        return jsonify({'success': False, 'error': 'Username is already taken'}), 400
    
    # Update username
    if db_change_username(current_user.id, new_username):
        return jsonify({'success': True, 'message': 'Username updated successfully', 'new_username': new_username})
    
    return jsonify({'success': False, 'error': 'Failed to update username'}), 500

@auth_bp.route("/user")
@login_required
def user():
    has_pfp = get_user_pfp(current_user.get_id()) is not None
    return render_template("user.html", page="user", has_pfp=has_pfp)

@auth_bp.route("/user/profile-picture", methods=["GET"])
@login_required
def get_profile_picture():
    """Return the user's profile picture as an image response"""
    pfp_data = get_user_pfp(current_user.get_id())
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
    if update_user_pfp(current_user.get_id(), file_data):
        return jsonify({'success': True, 'message': 'Profile picture updated successfully'})
    
    return jsonify({'error': 'Failed to update profile picture'}), 500

