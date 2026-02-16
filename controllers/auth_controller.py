"""Rutas de autenticación."""
from flask import Blueprint, request, redirect, url_for, session, render_template

from models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session.get("user_id"):
            return redirect(url_for("home.dashboard"))
        return render_template("auth/login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    if not username or not password:
        return render_template("auth/login.html", error="Usuario y contraseña requeridos")

    user = User.find_by_username(username)
    if not user or user.get("password") != password:
        return render_template("auth/login.html", error="Credenciales inválidas")

    session["user_id"] = user["id"]
    session["username"] = user["username"]
    return redirect(url_for("home.dashboard"))


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
