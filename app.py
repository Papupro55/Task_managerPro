"""Punto de entrada principal - Task Manager Legacy (MVC)."""
from flask import Flask
from config import SECRET_KEY, MONGODB_URI, MONGODB_DB
from models.database import init_db
from controllers.auth_controller import auth_bp
from controllers.home_controller import home_bp
from controllers.task_controller import task_bp
from controllers.project_controller import project_bp

app = Flask(__name__, template_folder="views", static_folder="static")
app.secret_key = SECRET_KEY
app.config["MONGODB_URI"] = MONGODB_URI
app.config["MONGODB_DB"] = MONGODB_DB

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(home_bp)
app.register_blueprint(task_bp, url_prefix="/tasks")
app.register_blueprint(project_bp, url_prefix="/projects")

# Inicializar conexión a MongoDB y datos por defecto
init_db(app)
with app.app_context():
    from models.user import User
    from models.project import Project
    User.ensure_default_users()
    Project.ensure_default()

@app.route("/")
def index():
    """Redirige a login o dashboard según sesión."""
    from flask import redirect, session
    if session.get("user_id"):
        return redirect("/dashboard")
    return redirect("/auth/login")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
