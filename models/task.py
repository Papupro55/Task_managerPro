"""Modelo Tarea, Comentarios, Historial y Notificaciones."""
from datetime import datetime
from .database import get_db


def _serialize(doc):
    if doc is None:
        return None
    d = dict(doc)
    d.pop("_id", None)
    return d


class Task:
    """Operaciones de tareas en MongoDB."""
    COLlection = "tasks"

    @staticmethod
    def get_all():
        db = get_db()
        return [_serialize(t) for t in db[Task.COLlection].find({})]

    @staticmethod
    def get_by_id(tid):
        db = get_db()
        return _serialize(db[Task.COLlection].find_one({"id": tid}))

    @staticmethod
    def add(data):
        db = get_db()
        last = db[Task.COLlection].find_one(sort=[("id", -1)])
        new_id = (last["id"] + 1) if last else 1
        now = datetime.utcnow().isoformat() + "Z"
        doc = {
            "id": new_id,
            "title": data.get("title", ""),
            "description": data.get("description", ""),
            "status": data.get("status", "Pendiente"),
            "priority": data.get("priority", "Media"),
            "projectId": data.get("projectId") or 0,
            "assignedTo": data.get("assignedTo") or 0,
            "dueDate": data.get("dueDate", ""),
            "estimatedHours": data.get("estimatedHours") or 0,
            "actualHours": data.get("actualHours") or 0,
            "createdBy": data.get("createdBy"),
            "createdAt": now,
            "updatedAt": now,
        }
        db[Task.COLlection].insert_one(doc)
        return new_id

    @staticmethod
    def update(tid, data):
        db = get_db()
        data["updatedAt"] = datetime.utcnow().isoformat() + "Z"
        allowed = {
            "title", "description", "status", "priority", "projectId",
            "assignedTo", "dueDate", "estimatedHours", "actualHours", "updatedAt"
        }
        update = {k: v for k, v in data.items() if k in allowed}
        result = db[Task.COLlection].update_one({"id": tid}, {"$set": update})
        return result.modified_count > 0

    @staticmethod
    def delete(tid):
        db = get_db()
        result = db[Task.COLlection].delete_one({"id": tid})
        return result.deleted_count > 0

    @staticmethod
    def search(text="", status="", priority="", project_id=0):
        db = get_db()
        q = {}
        if text:
            q["$or"] = [
                {"title": {"$regex": text, "$options": "i"}},
                {"description": {"$regex": text, "$options": "i"}},
            ]
        if status:
            q["status"] = status
        if priority:
            q["priority"] = priority
        if project_id and project_id > 0:
            q["projectId"] = project_id
        return [_serialize(t) for t in db[Task.COLlection].find(q)]


class Comment:
    COLlection = "comments"

    @staticmethod
    def get_by_task(tid):
        db = get_db()
        return list(db[Comment.COLlection].find({"taskId": tid}).sort("createdAt", 1))

    @staticmethod
    def add(task_id, user_id, comment_text):
        db = get_db()
        last = db[Comment.COLlection].find_one(sort=[("id", -1)])
        new_id = (last["id"] + 1) if last else 1
        doc = {
            "id": new_id,
            "taskId": task_id,
            "userId": user_id,
            "commentText": comment_text,
            "createdAt": datetime.utcnow().isoformat() + "Z",
        }
        db[Comment.COLlection].insert_one(doc)
        return new_id


class HistoryEntry:
    COLlection = "history"

    @staticmethod
    def get_by_task(tid):
        db = get_db()
        return list(db[HistoryEntry.COLlection].find({"taskId": tid}).sort("timestamp", -1))

    @staticmethod
    def get_all(limit=100):
        db = get_db()
        return list(db[HistoryEntry.COLlection].find({}).sort("timestamp", -1).limit(limit))

    @staticmethod
    def add(task_id, user_id, action, old_value="", new_value=""):
        db = get_db()
        last = db[HistoryEntry.COLlection].find_one(sort=[("id", -1)])
        new_id = (last["id"] + 1) if last else 1
        doc = {
            "id": new_id,
            "taskId": task_id,
            "userId": user_id,
            "action": action,
            "oldValue": old_value,
            "newValue": new_value,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        db[HistoryEntry.COLlection].insert_one(doc)


class Notification:
    COLlection = "notifications"

    @staticmethod
    def get_unread(user_id):
        db = get_db()
        return list(db[Notification.COLlection].find({"userId": user_id, "read": False}).sort("createdAt", -1))

    @staticmethod
    def add(user_id, message, ntype="info"):
        db = get_db()
        last = db[Notification.COLlection].find_one(sort=[("id", -1)])
        new_id = (last["id"] + 1) if last else 1
        doc = {
            "id": new_id,
            "userId": user_id,
            "message": message,
            "type": ntype,
            "read": False,
            "createdAt": datetime.utcnow().isoformat() + "Z",
        }
        db[Notification.COLlection].insert_one(doc)

    @staticmethod
    def mark_read(user_id):
        db = get_db()
        db[Notification.COLlection].update_many({"userId": user_id}, {"$set": {"read": True}})
