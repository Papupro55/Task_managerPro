"""Rutas principales (dashboard)."""
from functools import wraps
from flask import Blueprint, render_template, session, redirect, url_for, request

from models.user import User
from models.project import Project
from models.task import Task, Comment, HistoryEntry, Notification

home_bp = Blueprint("home", __name__)


def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return inner


@home_bp.route("/dashboard")
@login_required
def dashboard():
    """Panel principal con todas las pestañas (tareas, proyectos, etc.)."""
    users = User.get_all()
    projects = Project.get_all()
    tasks = Task.get_all()
    current_user = User.find_by_id(session["user_id"])
    stats = _compute_stats(tasks)

    # Datos opcionales según pestaña/parámetros
    comments_text = None
    history_text = None
    notifications_list = []
    search_results = None

    tab = request.args.get("tab", "")
    task_id = request.args.get("task_id", type=int)

    if tab == "comments" and task_id:
        comments = Comment.get_by_task(task_id)
        lines = [f"=== COMENTARIOS TAREA #{task_id} ===", ""]
        for c in comments:
            u = User.find_by_id(c.get("userId"))
            uname = u.get("username", "Usuario") if u else "Usuario"
            lines.append(f"[{c.get('createdAt', '')}] {uname}: {c.get('commentText', '')}")
            lines.append("---")
        comments_text = "\n".join(lines) if lines else "No hay comentarios"

    if tab == "history" and task_id:
        history = HistoryEntry.get_by_task(task_id)
        lines = [f"=== HISTORIAL TAREA #{task_id} ===", ""]
        for h in history:
            u = User.find_by_id(h.get("userId"))
            uname = u.get("username", "Desconocido") if u else "Desconocido"
            lines.append(f"{h.get('timestamp', '')} - {h.get('action', '')}")
            lines.append(f"  Usuario: {uname}")
            lines.append(f"  Antes: {h.get('oldValue', '(vacío)')}")
            lines.append(f"  Después: {h.get('newValue', '(vacío)')}")
            lines.append("---")
        history_text = "\n".join(lines) if lines else "No hay historial"
    elif tab == "history":
        history = HistoryEntry.get_all()
        lines = ["=== HISTORIAL COMPLETO ===", ""]
        for h in history:
            u = User.find_by_id(h.get("userId"))
            uname = u.get("username", "Desconocido") if u else "Desconocido"
            lines.append(f"Tarea #{h.get('taskId')} - {h.get('action')} - {h.get('timestamp')}")
            lines.append(f"  Usuario: {uname}")
            lines.append("---")
        history_text = "\n".join(lines) if lines else "No hay historial"

    if tab == "notifications":
        notifications_list = Notification.get_unread(session["user_id"])
        notifications_list = [f"• [{n.get('type')}] {n.get('message')} ({n.get('createdAt')})" for n in notifications_list]

    if tab == "search":
        search_text = request.args.get("q", "")
        search_status = request.args.get("status", "")
        search_priority = request.args.get("priority", "")
        search_project = request.args.get("project_id", 0, type=int)
        search_results = Task.search(search_text, search_status, search_priority, search_project)

    return render_template(
        "home/dashboard.html",
        current_user=current_user,
        users=users,
        projects=projects,
        tasks=tasks,
        stats=stats,
        comments_text=comments_text,
        history_text=history_text,
        notifications_list=notifications_list,
        search_results=search_results,
        tab=tab,
        task_id=task_id,
    )


def _compute_stats(tasks):
    total = len(tasks)
    completed = sum(1 for t in tasks if t.get("status") == "Completada")
    pending = total - completed
    high = sum(1 for t in tasks if t.get("priority") in ("Alta", "Crítica"))
    from datetime import datetime
    now = datetime.utcnow()
    overdue = 0
    for t in tasks:
        if t.get("dueDate") and t.get("status") != "Completada":
            try:
                due = datetime.fromisoformat(t["dueDate"].replace("Z", "+00:00"))
                if due.replace(tzinfo=None) < now:
                    overdue += 1
            except Exception:
                pass
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "high_priority": high,
        "overdue": overdue,
    }
