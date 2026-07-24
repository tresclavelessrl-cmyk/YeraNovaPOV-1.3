"""Ventana principal mejorada"""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QMenuBar,
    QStatusBar,
    QPushButton,
    QLabel,
    QSplitter,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QAction, QFont
from loguru import logger

from config.settings import settings
from ui.styles.theme import GestorTemas
from ui.windows.login import VentanaLogin
from ui.windows.ventas import VentanaVentas
from ui.windows.inventario import VentanaInventario
from database.models import Usuario


class MainWindow(QMainWindow):
    """Ventana principal de YeraPOV"""

    def __init__(self):
        """Inicializar ventana principal"""
        super().__init__()
        self.setWindowTitle("YeraPOV - Sistema POS e Inventario")
        
        # Configurar ventana
        ancho = settings.get("resolucion.ancho", 1200)
        alto = settings.get("resolucion.alto", 800)
        self.setMinimumSize(QSize(ancho, alto))
        
        if settings.get("maximizado", True):
            self.showMaximized()
        
        # Variable para usuario actual
        self.usuario_actual: Usuario = None
        
        # Crear interfaz
        self._create_ui()
        self._create_menu()
        self._create_status_bar()
        self._apply_theme()
        
        # Mostrar login
        self._mostrar_login()
        
        logger.info("Ventana principal creada")

    def _create_ui(self) -> None:
        """Crear interfaz de usuario"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
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
        action_nueva_venta.triggered.connect(self._ir_a_ventas)
        menu_archivo.addAction(action_nueva_venta)
        
        menu_archivo.addSeparator()
        
        action_cerrar_sesion = QAction("&Cerrar Sesión", self)
        action_cerrar_sesion.setShortcut("Ctrl+L")
        action_cerrar_sesion.triggered.connect(self._cerrar_sesion)
        menu_archivo.addAction(action_cerrar_sesion)
        
        menu_archivo.addSeparator()
        
        action_salir = QAction("&Salir", self)
        action_salir.setShortcut("Ctrl+Q")
        action_salir.triggered.connect(self.close)
        menu_archivo.addAction(action_salir)
        
        # Menú Ver
        menu_ver = menubar.addMenu("&Ver")
        
        action_ventas = QAction("&Ventas", self)
        action_ventas.setShortcut("Ctrl+1")
        action_ventas.triggered.connect(self._ir_a_ventas)
        menu_ver.addAction(action_ventas)
        
        action_inventario = QAction("&Inventario", self)
        action_inventario.setShortcut("Ctrl+2")
        action_inventario.triggered.connect(self._ir_a_inventario)
        menu_ver.addAction(action_inventario)
        
        # Menú Ayuda
        menu_ayuda = menubar.addMenu("&Ayuda")
        
        action_acerca = QAction("&Acerca de", self)
        menu_ayuda.addAction(action_acerca)

    def _create_status_bar(self) -> None:
        """Crear barra de estado"""
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Listo")

    def _apply_theme(self) -> None:
        """Aplicar tema de la aplicación"""
        tema = settings.get("tema", "oscuro")
        stylesheet = GestorTemas.obtener_stylesheet(tema)
        self.setStyleSheet(stylesheet)
        logger.info(f"Tema aplicado: {tema}")

    def _mostrar_login(self) -> None:
        """Mostrar pantalla de login"""
        self.stacked_widget.clear()
        
        ventana_login = VentanaLogin()
        ventana_login.usuario_autenticado.connect(self._usuario_autenticado)
        
        self.stacked_widget.addWidget(ventana_login)
        self.stacked_widget.setCurrentWidget(ventana_login)

    def _usuario_autenticado(self, usuario: Usuario) -> None:
        """Evento cuando usuario se autentica"""
        self.usuario_actual = usuario
        self.setWindowTitle(
            f"YeraPOV - Sistema POS | {usuario.nombre_completo} ({usuario.rol.value})"
        )
        self.statusbar.showMessage(f"Sesionado como: {usuario.nombre_completo}")
        
        # Mostrar pantalla de ventas
        self._ir_a_ventas()

    def _ir_a_ventas(self) -> None:
        """Ir a pantalla de ventas"""
        if not self.usuario_actual:
            self._mostrar_login()
            return
        
        self.stacked_widget.clear()
        
        ventana_ventas = VentanaVentas(self.usuario_actual)
        self.stacked_widget.addWidget(ventana_ventas)
        self.stacked_widget.setCurrentWidget(ventana_ventas)

    def _ir_a_inventario(self) -> None:
        """Ir a pantalla de inventario"""
        if not self.usuario_actual:
            self._mostrar_login()
            return
        
        self.stacked_widget.clear()
        
        ventana_inventario = VentanaInventario()
        self.stacked_widget.addWidget(ventana_inventario)
        self.stacked_widget.setCurrentWidget(ventana_inventario)

    def _cerrar_sesion(self) -> None:
        """Cerrar sesión del usuario actual"""
        self.usuario_actual = None
        self._mostrar_login()
