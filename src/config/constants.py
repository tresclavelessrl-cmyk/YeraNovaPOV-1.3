"""Constantes globales de la aplicación"""

from enum import Enum
from datetime import datetime

# Información de la aplicación
APP_NAME = "YeraPOV"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Tres Claveles S.R.L."
APP_DESCRIPTION = "Sistema POS e Inventario Multiplataforma"
DEFAULT_CURRENCY = "$"
CURRENCY_CODE = "ARS"  # Código de moneda ISO

# Configuración de Base de Datos
DB_NAME = "yerapov.db"
DB_BACKUP_DIR = "backups"
DB_BACKUP_INTERVAL = 3600  # Segundos (1 hora)

# Configuración de Tickets
class TICKET_WIDTHS(Enum):
    """Anchos de ticket disponibles"""
    MINI = 58  # mm
    STANDARD = 80  # mm

# Roles de usuario
class ROLES(Enum):
    """Roles de usuario en el sistema"""
    ADMINISTRADOR = "administrador"
    GERENTE = "gerente"
    VENDEDOR = "vendedor"
    ALMACENERO = "almacenero"
    CLIENTE = "cliente"

# Permisos por rol
PERMISOS = {
    ROLES.ADMINISTRADOR.value: [
        "crear_usuario",
        "editar_usuario",
        "eliminar_usuario",
        "ver_reportes_completos",
        "gestionar_inventario",
        "gestionar_caja",
        "realizar_venta",
        "crear_respaldo",
        "restaurar_respaldo",
        "acceder_configuracion",
    ],
    ROLES.GERENTE.value: [
        "ver_reportes_completos",
        "gestionar_inventario",
        "gestionar_caja",
        "realizar_venta",
        "crear_respaldo",
    ],
    ROLES.VENDEDOR.value: [
        "realizar_venta",
        "ver_reportes_personales",
    ],
    ROLES.ALMACENERO.value: [
        "gestionar_inventario",
        "ver_inventario",
    ],
}

# Estados de venta
class ESTADO_VENTA(Enum):
    """Estados posibles de una venta"""
    PENDIENTE = "pendiente"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"
    DEVUELTA = "devuelta"

# Estados de caja
class ESTADO_CAJA(Enum):
    """Estados de la caja registradora"""
    CERRADA = "cerrada"
    ABIERTA = "abierta"
    ARQUEO = "arqueo"

# Formatos de código de barras
class BARCODE_FORMATS(Enum):
    """Formatos de código de barras soportados"""
    EAN13 = "ean13"
    EAN8 = "ean8"
    CODE128 = "code128"
    CODE39 = "code39"
    UPCA = "upca"

# Formatos de exportación
class EXPORT_FORMATS(Enum):
    """Formatos de exportación disponibles"""
    EXCEL = "excel"
    PDF = "pdf"
    CSV = "csv"
    JSON = "json"

# Temas disponibles
class TEMAS(Enum):
    """Temas de interfaz disponibles"""
    CLARO = "claro"
    OSCURO = "oscuro"
    AUTO = "auto"

# Formato de fecha y hora
DATE_FORMAT = "%d/%m/%Y"
TIME_FORMAT = "%H:%M:%S"
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"

# Separadores para CSV/Excel
CSV_DELIMITER = ","
CSV_ENCODING = "utf-8"

# Límites de campo
LIMITS = {
    "nombre_usuario": 50,
    "contrasena_minima": 8,
    "descripcion_producto": 500,
    "codigo_barras": 50,
    "nombre_cliente": 100,
}

# Patrones de validación
PATTERNS = {
    "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    "telefono": r"^[\d\s\-\+\(\)]{10,20}$",
    "codigo_barras": r"^[\d]{8,15}$",
    "codigo_producto": r"^[A-Z0-9\-]{1,20}$",
}

# Configuración de API
API_TIMEOUT = 30  # segundos
API_RETRIES = 3
API_RETRY_DELAY = 1  # segundos

# Directorio de recursos
RESOURCES_DIR = "src/ui/resources"
ICONS_DIR = f"{RESOURCES_DIR}/icons"
ASSETS_DIR = f"{RESOURCES_DIR}/assets"

# Configuración de sincronización
SYNC_INTERVAL = 300  # 5 minutos
SYNC_BATCH_SIZE = 100
