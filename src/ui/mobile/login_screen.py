"""Pantalla de login para Kivy"""

from kivy.uix.screen import Screen
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from loguru import logger

from logic.autenticacion import SistemaAutenticacion


class LoginScreen(Screen):
    """Pantalla de login para dispositivo móvil"""

    def __init__(self, **kwargs):
        """Inicializar pantalla de login"""
        super().__init__(**kwargs)
        self.sistema_auth = SistemaAutenticacion()
        logger.info("Pantalla de login Kivy creada")

    def realizar_login(self, usuario: str, contrasena: str) -> None:
        """
        Realizar login
        
        Args:
            usuario: Nombre de usuario
            contrasena: Contraseña
        """
        if not usuario or not contrasena:
            self._mostrar_popup("Error", "Ingrese usuario y contraseña")
            return

        # Autenticar
        exitoso, usuario_obj, token = self.sistema_auth.autenticar(
            usuario, contrasena
        )

        if exitoso and usuario_obj:
            logger.info(f"Usuario autenticado (Kivy): {usuario}")
            # Ir a menú principal
            self.manager.get_screen("menu").usuario_autenticado = usuario_obj
            self.manager.current = "menu"
        else:
            self._mostrar_popup(
                "Error de autenticación",
                "Usuario o contraseña incorrectos",
            )

    @staticmethod
    def _mostrar_popup(titulo: str, mensaje: str) -> None:
        """
        Mostrar popup de alerta
        
        Args:
            titulo: Título del popup
            mensaje: Mensaje a mostrar
        """
        contenido = Label(text=mensaje)
        popup = Popup(
            title=titulo,
            content=contenido,
            size_hint=(0.9, 0.3),
        )
        popup.open()
