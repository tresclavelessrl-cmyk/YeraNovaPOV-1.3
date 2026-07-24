#!/usr/bin/env python3
"""Punto de entrada para Android (Kivy)"""

import os
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent))

from kivy.app import App
from kivy.core.window import Window
from loguru import logger

from config.settings import settings
from database.connection import init_db
from ui.screens.login_screen import LoginScreen


class YeraPOVApp(App):
    """Aplicación principal para Android"""

    def build(self):
        """Construir la aplicación"""
        logger.info(f"Iniciando YeraPOV v1.0.0 (Android)")
        logger.info(f"Configuración: {settings.config_dir}")
        logger.info(f"Base de datos: {settings.get_db_path()}")
        
        try:
            # Inicializar base de datos
            db = init_db()
            logger.info("Base de datos inicializada correctamente")
            
            # Configurar ventana
            Window.size = (480, 800)  # Tamaño móvil típico
            
            # Cargar tema
            tema = settings.get("tema", "claro")
            logger.info(f"Tema seleccionado: {tema}")
            
            # Retornar pantalla de login
            return LoginScreen()
            
        except Exception as e:
            logger.error(f"Error inicializando aplicación: {e}", exc_info=True)
            raise

    def on_stop(self):
        """Llamado cuando se cierra la aplicación"""
        logger.info("Cerrando aplicación")
        try:
            from database.connection import get_db
            db = get_db()
            db.close()
            logger.info("Base de datos cerrada")
        except:
            pass
        return True


if __name__ == "__main__":
    app = YeraPOVApp()
    app.run()
