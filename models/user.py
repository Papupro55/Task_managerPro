"""Modelo Usuario."""
from .database import get_db


class User:
    """Operaciones de usuarios en MongoDB."""
    COLlection = "users"

    @staticmethod
    def get_all():
        db = get_db()
        return list(db[User.COLlection].find({}, {"_id": 0, "id": 1, "username": 1, "password": 1}))

    @staticmethod
    def find_by_username(username):
        db = get_db()
        return db[User.COLlection].find_one({"username": username})

    @staticmethod
    def find_by_id(uid):
        db = get_db()
        u = db[User.COLlection].find_one({"id": uid})
        if u:
            u.pop("_id", None)
        return u

    @staticmethod
    def ensure_default_users():
        """Crea usuarios por defecto si no existen."""
        db = get_db()
        if db[User.COLlection].count_documents({}) == 0:
            default = [
                {"id": 1, "username": "admin", "password": "admin"},
                {"id": 2, "username": "user1", "password": "user1"},
                {"id": 3, "username": "user2", "password": "user2"},
            ]
            db[User.COLlection].insert_many(default)
