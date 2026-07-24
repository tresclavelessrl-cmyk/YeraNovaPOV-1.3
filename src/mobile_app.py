"""Aplicación Kivy principal para YeraPOV Mobile"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from loguru import logger

from ui.mobile.login_screen import LoginScreen
from ui.mobile.menu_screen import MenuScreen
from ui.mobile.ventas_screen import VentasScreen
from ui.mobile.inventario_screen import InventarioScreen

# Configurar ventana
Window.size = (540, 960)  # Dimensiones típicas de smartphone


class YeraPOVApp(App):
    """Aplicación Kivy para YeraPOV POS Mobile"""

    def build(self):
        """Construir aplicación"""
        # Crear gestor de pantallas
        sm = ScreenManager()

        # Crear y agregar pantallas
        login_screen = LoginScreen(name="login")
        menu_screen = MenuScreen(name="menu")
        ventas_screen = VentasScreen(name="ventas")
        inventario_screen = InventarioScreen(name="inventario")

        sm.add_widget(login_screen)
        sm.add_widget(menu_screen)
        sm.add_widget(ventas_screen)
        sm.add_widget(inventario_screen)

        logger.info("Aplicación Kivy construida")
        return sm

    def on_start(self):
        """Evento al iniciar la aplicación"""
        logger.info("Aplicación YeraPOV Mobile iniciada")

    def on_stop(self):
        """Evento al cerrar la aplicación"""
        logger.info("Aplicación YeraPOV Mobile cerrada")


if __name__ == "__main__":
    app = YeraPOVApp()
    app.run()
