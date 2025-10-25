from flask import Blueprint, flash, redirect, url_for, jsonify, render_template, request, get_flashed_messages
from flask_login import login_required, current_user, login_user, logout_user
from app.validations import validateRegister, validateLogin
from app.exceptions import RegisterError, LoginError
from app.services.db_info import register_new_user

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
        
        print(name)    
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
def user():
    return render_template("user.html", page="user")