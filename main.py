"""Punto de entrada principal de la aplicación"""

import sys
from pathlib import Path
from loguru import logger

# Configurar logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
logger.add(
    str(log_dir / "yerapov.log"),
    rotation="500 MB",
    retention="10 days",
    level="INFO",
)

def ejecutar_windows():
    """
    Ejecutar versión Windows (PySide6)
    """
    try:
        from PySide6.QtWidgets import QApplication
        from src.ui.windows.main_window import MainWindow

        app = QApplication(sys.argv)
        ventana = MainWindow()
        ventana.show()
        sys.exit(app.exec())
    except ImportError:
        logger.error("PySide6 no está instalado. Instale con: pip install PySide6")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error ejecutando versión Windows: {e}")
        sys.exit(1)


def ejecutar_mobile():
    """
    Ejecutar versión Mobile (Kivy)
    """
    try:
        from src.mobile_app import YeraPOVApp

        app = YeraPOVApp()
        app.run()
    except ImportError:
        logger.error("Kivy no está instalado. Instale con: pip install kivy")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error ejecutando versión Mobile: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="YeraPOV - Sistema POS e Inventario"
    )
    parser.add_argument(
        "--mobile",
        action="store_true",
        help="Ejecutar versión móvil (Kivy)",
    )
    parser.add_argument(
        "--windows",
        action="store_true",
        help="Ejecutar versión Windows (PySide6)",
    )

    args = parser.parse_args()

    if args.mobile:
        logger.info("Iniciando YeraPOV Mobile (Kivy)...")
        ejecutar_mobile()
    elif args.windows:
        logger.info("Iniciando YeraPOV Windows (PySide6)...")
        ejecutar_windows()
    else:
        # Por defecto, usar Windows si está disponible, sino Mobile
        try:
            import PySide6

            logger.info("Iniciando YeraPOV Windows (PySide6)...")
            ejecutar_windows()
        except ImportError:
            try:
                import kivy

                logger.info("Iniciando YeraPOV Mobile (Kivy)...")
                ejecutar_mobile()
            except ImportError:
                logger.error(
                    "Ni PySide6 ni Kivy están instalados.\n"
                    "Instale: pip install PySide6 kivy\n"
                    "o use: python main.py --windows o --mobile"
                )
                sys.exit(1)
