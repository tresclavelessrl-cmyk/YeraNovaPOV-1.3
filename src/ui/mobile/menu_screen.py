"""Pantalla de menú para Kivy"""

from kivy.uix.screen import Screen
from kivy.properties import StringProperty
from loguru import logger

from database.models import Usuario


class MenuScreen(Screen):
    """Pantalla de menú principal para dispositivo móvil"""

    usuario_actual = StringProperty("-")
    rol_actual = StringProperty("-")

    def __init__(self, **kwargs):
        """Inicializar pantalla de menú"""
        super().__init__(**kwargs)
        self.usuario_autenticado: Usuario = None
        logger.info("Pantalla de menú Kivy creada")

    def on_usuario_autenticado(self, usuario: Usuario) -> None:
        """
        Evento cuando se autentica un usuario
        
        Args:
            usuario: Usuario autenticado
        """
        self.usuario_autenticado = usuario
        self.usuario_actual = usuario.nombre_completo
        self.rol_actual = f"Rol: {usuario.rol.value}"
        logger.info(f"Usuario autenticado en menú: {usuario.nombre_completo}")

    def ir_ventas(self) -> None:
        """Ir a pantalla de ventas"""
        self.manager.get_screen("ventas").usuario_actual = (
            self.usuario_autenticado
        )
        self.manager.current = "ventas"
        logger.info("Navegando a ventas")

    def ir_inventario(self) -> None:
        """Ir a pantalla de inventario"""
        self.manager.current = "inventario"
        logger.info("Navegando a inventario")

    def buscar_codigo(self) -> None:
        """Buscar producto por código"""
        logger.info("Abriendo búsqueda de código")

    def configuracion(self) -> None:
        """Abrir configuración"""
        logger.info("Abriendo configuración")

    def cerrar_sesion(self) -> None:
        """Cerrar sesión"""
        self.usuario_autenticado = None
        self.usuario_actual = "-"
        self.rol_actual = "-"
        self.manager.current = "login"
        logger.info("Sesión cerrada")
