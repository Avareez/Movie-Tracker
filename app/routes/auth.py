from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from app.services.auth import register_user, authenticate_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user, error = register_user(username, password)
        if error:
            return render_template("register.html", error=error)
        
        return redirect(url_for("main.index"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user, error = authenticate_user(username, password)
        if error:
            return render_template("login.html", error=error)

        login_user(user)
        return redirect(url_for("main.index"))
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))