# Task Manager Legacy - Flask MVC

Sistema de gestión de tareas en **Flask** con patrón **Modelo-Vista-Controlador (MVC)** y base de datos **MongoDB**. Pensado para desplegar en **Render** con GitHub.

## Estructura del proyecto

```
legacyapp-main/
├── app.py                 # Punto de entrada principal
├── config.py              # Configuración (MongoDB, SECRET_KEY)
├── requirements.txt      # Dependencias
├── render.yaml            # Configuración para Render
│
├── models/                # MODELO (capa de datos)
│   ├── __init__.py
│   ├── database.py        # Conexión MongoDB
│   ├── user.py            # Usuario
│   ├── project.py         # Proyecto
│   └── task.py            # Tarea, Comentarios, Historial, Notificaciones
│
├── views/                 # VISTA (templates)
│   ├── layouts/
│   │   └── base.html
│   ├── auth/
│   │   └── login.html
│   └── home/
│       └── dashboard.html
│
├── controllers/           # CONTROLADOR (lógica de negocio)
│   ├── __init__.py
│   ├── auth_controller.py
│   ├── home_controller.py
│   ├── task_controller.py
│   └── project_controller.py
│
├── static/
│   ├── css/style.css
│   └── js/app.js
│
├── index.html             # (legacy - ya no se usa)
├── style.css              # (legacy - ver static/css/)
└── app.js                 # (legacy - ver static/js/)
```

## Funcionalidades

1. **Autenticación**: Login / logout con sesión
2. **CRUD de Tareas**: Crear, editar, eliminar tareas (MongoDB)
3. **CRUD de Proyectos**: Gestión de proyectos
4. **Comentarios**: Comentarios por tarea
5. **Historial**: Registro de cambios por tarea
6. **Notificaciones**: Por usuario
7. **Búsqueda**: Por texto, estado, prioridad, proyecto
8. **Reportes**: Resumen de tareas, proyectos y usuarios

## Uso local

1. Crear entorno virtual (recomendado):
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configurar MongoDB en `config.py` o con variable de entorno:
   ```bash
   set MONGODB_URI=mongodb+srv://...
   ```

4. Ejecutar la aplicación:
   ```bash
   python app.py
   ```
   Abre http://localhost:5000

5. Login por defecto: **admin** / **admin**

## Despliegue en Render

1. Sube el proyecto a **GitHub**.

2. En [Render](https://render.com): **New** → **Web Service**, conecta el repositorio.

3. Configuración:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

4. Variables de entorno:
   - **MONGODB_URI**: tu connection string de MongoDB Atlas (ej. `mongodb+srv://...@cluster0....mongodb.net/legacyapp?retryWrites=true&w=majority`)
   - **SECRET_KEY**: una clave secreta aleatoria (Render puede generarla)

5. La base de datos indicada en la URI es **legacyapp**; se crean usuarios y proyectos por defecto al arrancar si las colecciones están vacías.

## Datos por defecto

Al iniciar, si las colecciones están vacías se crean:

- **Usuarios**: admin/admin, user1/user1, user2/user2
- **Proyectos**: Proyecto Demo, Proyecto Alpha, Proyecto Beta

## Notas

- La app es 100% web: toda la lógica corre en el servidor (Flask + MongoDB).
- Los archivos `index.html`, `style.css` y `app.js` en la raíz son del proyecto original (localStorage); la versión actual usa `views/` y `static/`.
