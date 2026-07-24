"""Pantalla de login"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from loguru import logger

from logic.autenticacion import SistemaAutenticacion
from database.models import Usuario


class VentanaLogin(QWidget):
    """Ventana de login"""

    # Señal emitida cuando el usuario se autentica correctamente
    usuario_autenticado = Signal(Usuario)

    def __init__(self):
        """Inicializar ventana de login"""
        super().__init__()
        self.sistema_auth = SistemaAutenticacion()
        self.usuario_actual = None
        self._crear_ui()
        logger.info("Ventana de login creada")

    def _crear_ui(self) -> None:
        """Crear interfaz de usuario"""
        self.setWindowTitle("YeraPOV - Login")
        self.setGeometry(100, 100, 400, 300)
        self.setMaximumSize(400, 300)
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()

        # Título
        titulo = QLabel("YeraPOV")
        titulo_font = QFont()
        titulo_font.setPointSize(24)
        titulo_font.setBold(True)
        titulo.setFont(titulo_font)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        subtitulo = QLabel("Sistema POS")
        subtitulo_font = QFont()
        subtitulo_font.setPointSize(11)
        subtitulo.setFont(subtitulo_font)
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitulo)

        layout.addSpacing(20)

        # Usuario
        layout_usuario = QHBoxLayout()
        label_usuario = QLabel("Usuario:")
        label_usuario.setMinimumWidth(80)
        self.txt_usuario = QLineEdit()
        self.txt_usuario.setPlaceholderText("Ingrese su usuario")
        layout_usuario.addWidget(label_usuario)
        layout_usuario.addWidget(self.txt_usuario)
        layout.addLayout(layout_usuario)

        # Contraseña
        layout_contrasena = QHBoxLayout()
        label_contrasena = QLabel("Contraseña:")
        label_contrasena.setMinimumWidth(80)
        self.txt_contrasena = QLineEdit()
        self.txt_contrasena.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_contrasena.setPlaceholderText("Ingrese su contraseña")
        layout_contrasena.addWidget(label_contrasena)
        layout_contrasena.addWidget(self.txt_contrasena)
        layout.addLayout(layout_contrasena)

        layout.addSpacing(10)

        # Botón de login
        self.btn_login = QPushButton("Iniciar Sesión")
        self.btn_login.clicked.connect(self._realizar_login)
        self.btn_login.setMinimumHeight(35)
        layout.addWidget(self.btn_login)

        # Tecla Enter para login
        self.txt_contrasena.returnPressed.connect(self._realizar_login)

        layout.addStretch()

        self.setLayout(layout)

    def _realizar_login(self) -> None:
        """Realizar login"""
        usuario = self.txt_usuario.text().strip()
        contrasena = self.txt_contrasena.text()

        if not usuario or not contrasena:
            QMessageBox.warning(
                self,
                "Campos vacíos",
                "Por favor, ingrese usuario y contraseña",
            )
            return

        # Autenticar
        exitoso, usuario_obj, token = self.sistema_auth.autenticar(
            usuario, contrasena
        )

        if exitoso and usuario_obj:
            self.usuario_actual = usuario_obj
            logger.info(f"Usuario autenticado: {usuario}")
            self.usuario_autenticado.emit(usuario_obj)
            self.limpiar_campos()
        else:
            QMessageBox.critical(
                self,
                "Error de autenticación",
                "Usuario o contraseña incorrectos",
            )
            self.txt_contrasena.clear()
            self.txt_usuario.setFocus()

    def limpiar_campos(self) -> None:
        """Limpiar campos de entrada"""
        self.txt_usuario.clear()
        self.txt_contrasena.clear()
