#!/usr/bin/env python3
"""Punto de entrada para Windows (PySide6)"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread
from loguru import logger

from config.settings import settings
from database.connection import init_db
from ui.windows.main_window import MainWindow


def main():
    """Función principal"""
    logger.info(f"Iniciando YeraPOV v1.0.0")
    logger.info(f"Configuración: {settings.config_dir}")
    logger.info(f"Base de datos: {settings.get_db_path()}")
    
    try:
        # Inicializar base de datos
        db = init_db()
        logger.info("Base de datos inicializada correctamente")
        
        # Crear aplicación Qt
        app = QApplication(sys.argv)
        
        # Cargar tema
        tema = settings.get("tema", "claro")
        logger.info(f"Tema seleccionado: {tema}")
        
        # Crear ventana principal
        ventana_principal = MainWindow()
        ventana_principal.show()
        
        logger.info("Aplicación iniciada correctamente")
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Error iniciando aplicación: {e}", exc_info=True)
        sys.exit(1)
    finally:
        # Cerrar base de datos
        try:
            db = get_db()
            db.close()
            logger.info("Base de datos cerrada")
        except:
            pass


if __name__ == "__main__":
    main()
