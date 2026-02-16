"""Rutas de proyectos."""
from flask import Blueprint, request, redirect, url_for, session

from models.project import Project

project_bp = Blueprint("projects", __name__)


def _login_required(f):
    from functools import wraps
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return inner


@project_bp.route("/add", methods=["POST"])
@_login_required
def add():
    name = request.form.get("projectName", "").strip()
    description = request.form.get("projectDescription", "")
    if name:
        Project.add(name, description)
    return redirect(url_for("home.dashboard") + "#projects")


@project_bp.route("/update/<int:pid>", methods=["POST"])
@_login_required
def update(pid):
    name = request.form.get("projectName", "").strip()
    description = request.form.get("projectDescription", "")
    if name:
        Project.update(pid, name, description)
    return redirect(url_for("home.dashboard") + "#projects")


@project_bp.route("/delete/<int:pid>", methods=["POST"])
@_login_required
def delete(pid):
    Project.delete(pid)
    return redirect(url_for("home.dashboard") + "#projects")
