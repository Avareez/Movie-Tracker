from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.db_models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error = "Username already taken."
            return render_template("register.html", error=error)
        
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("main.index"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            error = "Invalid username or password."
            return render_template("login.html", error=error)
        
        return redirect(url_for("main.index"))
    return render_template("login.html")