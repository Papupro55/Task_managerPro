"""Configuración de MongoDB."""
from pymongo import MongoClient
from config import MONGODB_URI, MONGODB_DB

_client = None
_db = None


def init_db(app):
    """Inicializa la conexión a MongoDB con la app Flask."""
    global _client, _db
    _client = MongoClient(app.config.get("MONGODB_URI", MONGODB_URI))
    _db = _client[app.config.get("MONGODB_DB", MONGODB_DB)]
    try:
        _db.users.create_index("username", unique=True)
    except Exception:
        pass
    try:
        _db.tasks.create_index("projectId")
        _db.tasks.create_index("assignedTo")
    except Exception:
        pass
    return _db


def get_db():
    """Devuelve la instancia de la base de datos."""
    global _db
    if _db is None:
        from config import MONGODB_URI, MONGODB_DB
        _client = MongoClient(MONGODB_URI)
        _db = _client[MONGODB_DB]
    return _db
