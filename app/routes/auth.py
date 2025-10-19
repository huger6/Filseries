from flask import Blueprint, flash, redirect, url_for, jsonify, render_template, request, get_flashed_messages
from flask_login import login_required, current_user, login_user, logout_user
from app.validations import validateRegister, validateLogin
from app.exceptions import RegisterError, LoginError

auth_bp = Blueprint("auth", __name__, template_folder='../templates/auth')


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == "POST":
        username = request.form.get("username")
        pw = request.form.get("password")

        try:
            if validateLogin(username, pw):
                return redirect(url_for('main.home'))
        except LoginError as e:
            return render_template("login.html", page="login", error=e)

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
        name = request.form.get("Name")
        username = request.form.get("username")
        pw = request.form.get("password")
        pw_confirm = request.form.get("confirm_password")

        try:
            if validateRegister(username, name, pw, pw_confirm):
                return redirect(url_for('auth.login'))
        except RegisterError as e:
            return render_template("register.html", page="register", error=e)

    return render_template("register.html", page="register")

@auth_bp.route("/change-password")
def change_password():
    return render_template("changePassword.html", pages="change-password")

def validateRegisterInfo():
    return True