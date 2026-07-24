"""Módulo de configuración"""

from .settings import Settings
from .constants import (
    APP_NAME,
    APP_VERSION,
    DEFAULT_CURRENCY,
    TICKET_WIDTHS,
    ROLES,
    PERMISOS,
)

__all__ = [
    "Settings",
    "APP_NAME",
    "APP_VERSION",
    "DEFAULT_CURRENCY",
    "TICKET_WIDTHS",
    "ROLES",
    "PERMISOS",
]
