"""Modelo Proyecto."""
from .database import get_db


class Project:
    """Operaciones de proyectos en MongoDB."""
    COLlection = "projects"

    @staticmethod
    def get_all():
        db = get_db()
        return list(db[Project.COLlection].find({}, {"_id": 0}))

    @staticmethod
    def get_by_id(pid):
        db = get_db()
        p = db[Project.COLlection].find_one({"id": pid})
        if p:
            p.pop("_id", None)
        return p

    @staticmethod
    def add(name, description=""):
        db = get_db()
        last = db[Project.COLlection].find_one(sort=[("id", -1)])
        new_id = (last["id"] + 1) if last else 1
        doc = {"id": new_id, "name": name, "description": description or ""}
        db[Project.COLlection].insert_one(doc)
        return new_id

    @staticmethod
    def update(pid, name, description=""):
        db = get_db()
        result = db[Project.COLlection].update_one(
            {"id": pid},
            {"$set": {"name": name, "description": description or ""}}
        )
        return result.modified_count > 0

    @staticmethod
    def delete(pid):
        db = get_db()
        result = db[Project.COLlection].delete_one({"id": pid})
        return result.deleted_count > 0

    @staticmethod
    def ensure_default():
        """Crea proyectos por defecto si no existen."""
        db = get_db()
        if db[Project.COLlection].count_documents({}) == 0:
            default = [
                {"id": 1, "name": "Proyecto Demo", "description": "Proyecto de ejemplo"},
                {"id": 2, "name": "Proyecto Alpha", "description": "Proyecto importante"},
                {"id": 3, "name": "Proyecto Beta", "description": "Proyecto secundario"},
            ]
            db[Project.COLlection].insert_many(default)
