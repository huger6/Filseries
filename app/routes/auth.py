from flask import Blueprint, flash, redirect, url_for, jsonify, render_template, request
from flask_login import login_required, current_user, login_user, logout_user
from app.models.models import bcrypt, db, User

auth_bp = Blueprint("auth_bp", __name__, template_folder='../templates/auth')

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # if current_user.is_authenticated:
    #     flash("User is authenticated in register path")
    #     redirect(url_for("app.home"))

    # form = RegisterForm()

    # if form.validate_on_submit():
    #     User.create_user(email=form.email.data, username=form.username.data, password=form.password.data)
    #     return redirect(url_for("app.login"))
    
    return render_template("register.html", form=form)
    
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    #User is already logged in
    if current_user.is_authenticated:
        return redirect(url_for("app.home"))
    
    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.username.data).first() #Might cause a BUG if there are many identical emails
    #     if user:
    #         if bcrypt.check_password_hash(user.pass_hash, form.password.data):
    #             login_user(user)
    #             return redirect(url_for("app.home"))
    #         else:
    #             flash("Invalid email")
    
    return render_template("login.html", form=form)  

@auth_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    if current_user.get_id() == None:
        return redirect(url_for('app.home'))
    logout_user()
    return render_template("logout.html")

# @auth_bp.route("/change-password", methods=["GET", "POST"])
# @login_required
# def change_password():
#     if request.method == "POST":
#         old_password = request.form["old_password"]
#         new_password = request.form["new_password"]

#         if not bcrypt.check_password_hash(current_user.pass_hash, old_password):
#             return redirect(url_for("app.change-password"))
        
#         hashed_new_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
#         current_user.pass_hash = hashed_new_password
#         db.session.commit()

#         flash("Password alterada com sucesso!", "sucess")
#         return redirect(url_for("app.home"))
    
#     return render_template()  #TODO