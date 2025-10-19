from flask import Flask, render_template
import os
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__, template_folder="../app/templates")

@app.route("/")
def home():
    return render_template("main/home.html", page="home")

@app.route("/about")
def about():
    return render_template("../app/templates/main/about.html", page="about")

@app.route("/watchlist")
def watchlist():
    return render_template("../app/templates/watchlist/watchlist.html", page="watchlist")

@app.route("/login")
def login():
    return render_template("../app/templates/auth/login.html", page="login")

@app.route("/logout")
def logout():
    return render_template("../app/templates/auth/logout.html", page="logout")

@app.route("/register")
def register():
    return render_template("../app/templates/auth/register.html", page="register")

if __name__ == "__main__":
    app.run(debug=True)