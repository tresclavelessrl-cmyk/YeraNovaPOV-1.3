"""Configuración para aplicación móvil"""

from pathlib import Path
import os

# Resolución de pantalla
RES_ANCHO = 540
RES_ALTO = 960

# Colores
COLOR_PRIMARIO = (0.11, 0.27, 0.53, 1)  # #1f4788
COLOR_SECUNDARIO = (0.31, 0.78, 0.47, 1)  # #4CAF50
COLOR_ADVERTENCIA = (0.8, 0.6, 0.2, 1)  # Naranja
COLOR_ERROR = (0.8, 0.2, 0.2, 1)  # Rojo

# Rutas
BASE_DIR = Path(__file__).parent.parent
KV_DIR = BASE_DIR / "src" / "ui" / "kv"
DATA_DIR = BASE_DIR / "data"

# Dimensiones de fuente
FONT_GRANDE = "24sp"
FONT_NORMAL = "16sp"
FONT_PEQUENO = "12sp"

# Temas
TEMAS_DISPONIBLES = ["oscuro", "claro"]
TEMA_DEFECTO = "oscuro"

# Configuración de base de datos móvil
DB_PATH = DATA_DIR / "yerapov_mobile.db"
DB_TIMEOUT = 30  # Segundos

# Sincronización
ENABLE_SYNC = True
SYNC_INTERVAL = 300  # Segundos (5 minutos)

# Almacenamiento en caché
ENABLE_CACHE = True
CACHE_MAX_SIZE = 100  # MB
