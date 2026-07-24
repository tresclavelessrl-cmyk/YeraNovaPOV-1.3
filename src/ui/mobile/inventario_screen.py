"""Pantalla de inventario para Kivy"""

from kivy.uix.screen import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from loguru import logger

from logic.inventario import GestorInventario
from config.constants import DEFAULT_CURRENCY


class InventarioScreen(Screen):
    """Pantalla de inventario para dispositivo móvil"""

    def __init__(self, **kwargs):
        """Inicializar pantalla de inventario"""
        super().__init__(**kwargs)
        self.gestor_inventario = GestorInventario()
        self._cargar_productos()
        logger.info("Pantalla de inventario Kivy creada")

    def _cargar_productos(self) -> None:
        """Cargar productos"""
        try:
            session = self.gestor_inventario.db.get_session()
            productos = session.query(
                self.gestor_inventario.db.get_session()
                .query(type(None))
                .statement.froms[0]
            ).all()
            session.close()

            self.ids.grid_productos.clear_widgets()

            for producto in productos:
                item = self._crear_item_producto(producto)
                self.ids.grid_productos.add_widget(item)
        except Exception as e:
            logger.error(f"Error cargando productos: {e}")

    @staticmethod
    def _crear_item_producto(producto) -> BoxLayout:
        """
        Crear widget de producto
        
        Args:
            producto: Objeto producto
            
        Returns:
            BoxLayout con información del producto
        """
        layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="80dp",
            spacing="10dp",
            padding="10dp",
        )

        # Información del producto
        info_layout = BoxLayout(orientation="vertical")
        info_layout.add_widget(
            Label(
                text=f"[b]{producto.nombre}[/b]",
                markup=True,
                size_hint_y=0.5,
            )
        )
        info_layout.add_widget(
            Label(
                text=f"Stock: {producto.stock_actual} | Precio: {DEFAULT_CURRENCY}{producto.precio_venta:.2f}",
                size_hint_y=0.5,
                font_size="12sp",
            )
        )

        layout.add_widget(info_layout)

        # Botones de acción
        btn_layout = BoxLayout(size_hint_x=0.3, spacing="5dp")
        btn_layout.add_widget(Button(text="Edit", size_hint_x=0.5))
        btn_layout.add_widget(Button(text="Stock", size_hint_x=0.5))

        layout.add_widget(btn_layout)

        return layout

    def filtrar_productos(self, texto: str) -> None:
        """
        Filtrar productos
        
        Args:
            texto: Texto de búsqueda
        """
        # Implementar filtrado de productos
        logger.info(f"Filtrando productos: {texto}")

    def nuevo_producto(self) -> None:
        """Crear nuevo producto"""
        self._mostrar_alerta("Información", "Función en desarrollo")

    def ir_menu(self) -> None:
        """Volver a menú"""
        self.manager.current = "menu"

    @staticmethod
    def _mostrar_alerta(titulo: str, mensaje: str) -> None:
        """
        Mostrar alerta
        
        Args:
            titulo: Título
            mensaje: Mensaje
        """
        contenido = BoxLayout(orientation="vertical", padding="10dp", spacing="10dp")
        contenido.add_widget(Label(text=mensaje))

        btn_ok = Button(text="OK", size_hint_y=0.3)
        contenido.add_widget(btn_ok)

        popup = Popup(
            title=titulo,
            content=contenido,
            size_hint=(0.9, 0.4),
        )
        btn_ok.bind(on_press=popup.dismiss)
        popup.open()
