"""Configuración de la aplicación."""
import os

# MongoDB: en producción (Render) usar variable de entorno MONGODB_URI
MONGODB_URI = os.environ.get(
    "MONGODB_URI",
    "mongodb+srv://CoringaFem:1mDAqwHCVqGhtChO@cluster0.hw9jito.mongodb.net/legacyapp?retryWrites=true&w=majority"
)
MONGODB_DB = "legacyapp"

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
