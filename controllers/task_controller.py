"""Rutas de tareas, comentarios, historial, notificaciones, búsqueda y reportes."""
from flask import Blueprint, request, redirect, url_for, session, render_template

from models.user import User
from models.project import Project
from models.task import Task, Comment, HistoryEntry, Notification
import csv
import io
from flask import send_file

task_bp = Blueprint("tasks", __name__)


def _login_required(f):
    from functools import wraps
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return inner


def _context():
    return {
        "users": User.get_all(),
        "projects": Project.get_all(),
        "tasks": Task.get_all(),
        "current_user": User.find_by_id(session["user_id"]),
    }


@task_bp.route("/add", methods=["POST"])
@_login_required
def add():
    data = {
        "title": request.form.get("taskTitle", "").strip(),
        "description": request.form.get("taskDescription", ""),
        "status": request.form.get("taskStatus", "Pendiente"),
        "priority": request.form.get("taskPriority", "Media"),
        "projectId": int(request.form.get("taskProject") or 0),
        "assignedTo": int(request.form.get("taskAssigned") or 0),
        "dueDate": request.form.get("taskDueDate", ""),
        "estimatedHours": float(request.form.get("taskHours") or 0),
        "createdBy": session["user_id"],
    }
    if not data["title"]:
        return redirect(url_for("home.dashboard") + "#tasks")
    tid = Task.add(data)
    HistoryEntry.add(tid, session["user_id"], "CREATED", "", data["title"])
    if data["assignedTo"]:
        Notification.add(data["assignedTo"], "Nueva tarea asignada: " + data["title"], "task_assigned")
    return redirect(url_for("home.dashboard") + "#tasks")


@task_bp.route("/update/<int:tid>", methods=["POST"])
@_login_required
def update(tid):
    old = Task.get_by_id(tid)
    if not old:
        return redirect(url_for("home.dashboard"))
    data = {
        "title": request.form.get("taskTitle", "").strip(),
        "description": request.form.get("taskDescription", ""),
        "status": request.form.get("taskStatus", "Pendiente"),
        "priority": request.form.get("taskPriority", "Media"),
        "projectId": int(request.form.get("taskProject") or 0),
        "assignedTo": int(request.form.get("taskAssigned") or 0),
        "dueDate": request.form.get("taskDueDate", ""),
        "estimatedHours": float(request.form.get("taskHours") or 0),
        "actualHours": old.get("actualHours") or 0,
    }
    if not data["title"]:
        return redirect(url_for("home.dashboard") + "#tasks")
    if old.get("status") != data["status"]:
        HistoryEntry.add(tid, session["user_id"], "STATUS_CHANGED", old.get("status", ""), data["status"])
    if old.get("title") != data["title"]:
        HistoryEntry.add(tid, session["user_id"], "TITLE_CHANGED", old.get("title", ""), data["title"])
    Task.update(tid, data)
    if data["assignedTo"]:
        Notification.add(data["assignedTo"], "Tarea actualizada: " + data["title"], "task_updated")
    return redirect(url_for("home.dashboard") + "#tasks")


@task_bp.route("/delete/<int:tid>", methods=["POST"])
@_login_required
def delete(tid):
    task = Task.get_by_id(tid)
    if task:
        HistoryEntry.add(tid, session["user_id"], "DELETED", task.get("title", ""), "")
        Task.delete(tid)
    return redirect(url_for("home.dashboard") + "#tasks")


@task_bp.route("/comment", methods=["POST"])
@_login_required
def add_comment():
    task_id = int(request.form.get("commentTaskId") or 0)
    text = request.form.get("commentText", "").strip()
    if task_id and text:
        Comment.add(task_id, session["user_id"], text)
    return redirect(url_for("home.dashboard") + "#comments")


@task_bp.route("/notifications/read", methods=["POST"])
@_login_required
def mark_notifications_read():
    Notification.mark_read(session["user_id"])
    return redirect(url_for("home.dashboard") + "#notifications")

@task_bp.route("/export_reports")
@_login_required
def export_reports():

    context = _context()
    tasks = context["tasks"]
    projects = context["projects"]
    users = context["users"]

    total = len(tasks)
    completed = len([t for t in tasks if t.get("status") == "Completada"])
    pending = len([t for t in tasks if t.get("status") == "Pendiente"])

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Tipo", "Nombre", "Cantidad"])

    # Estadísticas generales
    writer.writerow(["Tareas Totales", "", total])
    writer.writerow(["Tareas Completadas", "", completed])
    writer.writerow(["Tareas Pendientes", "", pending])

    # Proyectos
    for p in projects:
        tareas_proyecto = len([t for t in tasks if t.get("projectId") == p.get("id")])
        writer.writerow(["Proyecto", p.get("name"), tareas_proyecto])

    # Usuarios
    for u in users:
        tareas_usuario = len([t for t in tasks if t.get("assignedTo") == u.get("id")])
        writer.writerow(["Usuario", u.get("username"), tareas_usuario])

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="reporte.csv"
    )