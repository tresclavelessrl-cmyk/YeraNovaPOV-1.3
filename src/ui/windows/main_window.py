"""Ventana principal de la aplicación"""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QMenuBar,
    QStatusBar,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QAction
from loguru import logger

from config.settings import settings


class MainWindow(QMainWindow):
    """Ventana principal de YeraPOV"""

    def __init__(self):
        """Inicializar ventana principal"""
        super().__init__()
        self.setWindowTitle("YeraPOV - Sistema POS")
        
        # Configurar ventana
        ancho = settings.get("resolucion.ancho", 1200)
        alto = settings.get("resolucion.alto", 800)
        self.setMinimumSize(QSize(ancho, alto))
        
        if settings.get("maximizado", True):
            self.showMaximized()
        
        # Crear interfaz
        self._create_ui()
        self._create_menu()
        self._create_status_bar()
        
        logger.info("Ventana principal creada")

    def _create_ui(self) -> None:
        """Crear interfaz de usuario"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Widget apilado para múltiples vistas
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)
        
        central_widget.setLayout(main_layout)

    def _create_menu(self) -> None:
        """Crear barra de menú"""
        menubar = self.menuBar()
        
        # Menú Archivo
        menu_archivo = menubar.addMenu("&Archivo")
        
        action_nueva_venta = QAction("&Nueva Venta", self)
        action_nueva_venta.setShortcut("Ctrl+N")
        menu_archivo.addAction(action_nueva_venta)
        
        menu_archivo.addSeparator()
        
        action_salir = QAction("&Salir", self)
        action_salir.setShortcut("Ctrl+Q")
        action_salir.triggered.connect(self.close)
        menu_archivo.addAction(action_salir)
        
        # Menú Ver
        menu_ver = menubar.addMenu("&Ver")
        
        # Menú Ayuda
        menu_ayuda = menubar.addMenu("&Ayuda")
        
        action_acerca = QAction("&Acerca de", self)
        menu_ayuda.addAction(action_acerca)

    def _create_status_bar(self) -> None:
        """Crear barra de estado"""
        statusbar = self.statusBar()
        statusbar.showMessage("Listo")

    def closeEvent(self, event):
        """Evento al cerrar ventana"""
        logger.info("Cerrando aplicación")
        event.accept()
