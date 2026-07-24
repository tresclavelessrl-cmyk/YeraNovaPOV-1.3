"""Temas para la aplicación"""

from enum import Enum
from .styles import DARK_STYLESHEET, LIGHT_STYLESHEET


class TemaActual(Enum):
    """Enum de temas disponibles"""
    CLARO = "claro"
    OSCURO = "oscuro"


class GestorTemas:
    """Gestor de temas de la aplicación"""

    TEMAS = {
        TemaActual.OSCURO.value: DARK_STYLESHEET,
        TemaActual.CLARO.value: LIGHT_STYLESHEET,
    }

    @staticmethod
    def obtener_stylesheet(tema: str) -> str:
        """
        Obtener stylesheet para un tema
        
        Args:
            tema: Nombre del tema
            
        Returns:
            Stylesheet QSS
        """
        return GestorTemas.TEMAS.get(tema, DARK_STYLESHEET)
