"""Gestión de configuración de la aplicación"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from loguru import logger
from .constants import (
    APP_NAME,
    TEMAS,
    DB_NAME,
    DEFAULT_CURRENCY,
    SYNC_INTERVAL,
)


class Settings:
    """Clase para gestionar la configuración de la aplicación"""

    def __init__(self):
        """Inicializar configuración"""
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / "config.json"
        self.db_dir = self._get_db_dir()
        self.backup_dir = self._get_backup_dir()

        # Cargar o crear configuración por defecto
        self.config = self._load_config()

    def _get_config_dir(self) -> Path:
        """Obtener directorio de configuración según SO"""
        if os.name == "nt":  # Windows
            config_path = Path(os.getenv("APPDATA")) / APP_NAME
        else:  # Linux/Android
            config_path = Path.home() / f".{APP_NAME.lower()}"

        config_path.mkdir(parents=True, exist_ok=True)
        return config_path

    def _get_db_dir(self) -> Path:
        """Obtener directorio de base de datos"""
        db_path = self.config_dir / "data"
        db_path.mkdir(parents=True, exist_ok=True)
        return db_path

    def _get_backup_dir(self) -> Path:
        """Obtener directorio de respaldos"""
        backup_path = self.config_dir / "backups"
        backup_path.mkdir(parents=True, exist_ok=True)
        return backup_path

    def _load_config(self) -> Dict[str, Any]:
        """Cargar configuración desde archivo o crear por defecto"""
        default_config = {
            "tema": TEMAS.CLARO.value,
            "moneda": DEFAULT_CURRENCY,
            "idioma": "es",
            "resolucion": {"ancho": 1200, "alto": 800},
            "maximizado": True,
            "sincronizacion": {
                "habilitada": True,
                "intervalo": SYNC_INTERVAL,
                "url_servidor": "",
                "auto_backup": True,
            },
            "tickets": {
                "ancho": 80,
                "mostrar_hora": True,
                "mostrar_vendedor": True,
            },
            "usuarios": {
                "requiere_contrasena_fuerte": True,
                "sesion_timeout": 1800,  # 30 minutos
            },
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    loaded_config = json.load(f)
                    # Fusionar con configuración por defecto
                    default_config.update(loaded_config)
                    logger.info(f"Configuración cargada: {self.config_file}")
            except Exception as e:
                logger.error(f"Error cargando configuración: {e}")
                logger.info("Usando configuración por defecto")
        else:
            self.save_config(default_config)

        return default_config

    def save_config(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Guardar configuración a archivo"""
        if config:
            self.config = config

        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
                logger.info(f"Configuración guardada: {self.config_file}")
        except Exception as e:
            logger.error(f"Error guardando configuración: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Obtener valor de configuración"""
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """Establecer valor de configuración"""
        keys = key.split(".")
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value
        self.save_config()

    def get_db_path(self) -> str:
        """Obtener ruta completa a la base de datos"""
        return str(self.db_dir / DB_NAME)

    def get_backup_path(self, filename: str) -> str:
        """Obtener ruta completa para archivo de respaldo"""
        return str(self.backup_dir / filename)

    def __repr__(self) -> str:
        """Representación en string"""
        return f"<Settings config_dir={self.config_dir} db_dir={self.db_dir}>"


# Instancia global de configuración
settings = Settings()
