"""YeraPOV - Sistema POS e Inventario Multiplataforma"""

__version__ = "1.0.0"
__author__ = "Tres Claveles S.R.L."
__license__ = "Boost Software License 1.0"

from loguru import logger
import sys

# Configurar logger
logger.remove()
logger.add(
    sys.stderr,
    format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
)

__all__ = ["logger", "__version__", "__author__", "__license__"]
