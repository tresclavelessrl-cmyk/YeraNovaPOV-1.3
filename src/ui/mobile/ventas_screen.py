"""Pantalla de ventas para Kivy"""

from kivy.uix.screen import Screen
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from loguru import logger

from database.models import Usuario
from logic.ventas import GestorVentas
from logic.inventario import GestorInventario
from logic.calculos import CalculosVenta
from config.constants import DEFAULT_CURRENCY


class VentasScreen(Screen):
    """Pantalla de ventas para dispositivo móvil"""

    producto_actual = StringProperty("-")
    precio_actual = StringProperty("-")
    stock_actual = StringProperty("-")
    subtotal_actual = StringProperty(f"{DEFAULT_CURRENCY}0.00")
    total_actual = StringProperty(f"{DEFAULT_CURRENCY}0.00")

    def __init__(self, usuario_actual: Usuario = None, **kwargs):
        """Inicializar pantalla de ventas"""
        super().__init__(**kwargs)
        self.usuario_actual = usuario_actual
        self.gestor_ventas = GestorVentas()
        self.gestor_inventario = GestorInventario()
        self.items_carrito = []
        self.cantidad_actual = 1
        self.producto_seleccionado = None
        logger.info("Pantalla de ventas Kivy creada")

    def buscar_producto(self, codigo: str) -> None:
        """
        Buscar producto por código de barras
        
        Args:
            codigo: Código de barras
        """
        if not codigo:
            self._mostrar_alerta("Advertencia", "Ingrese un código")
            return

        producto = self.gestor_inventario.obtener_producto_por_codigo_barras(
            codigo
        )

        if producto:
            self.producto_seleccionado = producto
            self.producto_actual = producto.nombre
            self.precio_actual = f"{DEFAULT_CURRENCY}{producto.precio_venta:.2f}"
            self.stock_actual = f"{producto.stock_actual} unidades"
            self.cantidad_actual = 1
            self.ids.txt_cantidad.text = "1"
            self.ids.txt_codigo.text = ""
            logger.info(f"Producto encontrado: {producto.nombre}")
        else:
            self._mostrar_alerta(
                "Producto no encontrado",
                f"No se encontró producto con código: {codigo}",
            )
            self.ids.txt_codigo.text = ""

    def cambiar_cantidad(self, delta: int) -> None:
        """
        Cambiar cantidad
        
        Args:
            delta: Cantidad a sumar/restar
        """
        try:
            cantidad = int(self.ids.txt_cantidad.text)
            nueva_cantidad = cantidad + delta

            if self.producto_seleccionado:
                if nueva_cantidad > self.producto_seleccionado.stock_actual:
                    nueva_cantidad = self.producto_seleccionado.stock_actual

            if nueva_cantidad > 0:
                self.ids.txt_cantidad.text = str(nueva_cantidad)
                self.cantidad_actual = nueva_cantidad
        except ValueError:
            self.ids.txt_cantidad.text = "1"
            self.cantidad_actual = 1

    def agregar_al_carrito(self) -> None:
        """Agregar producto al carrito"""
        if not self.producto_seleccionado:
            self._mostrar_alerta(
                "Advertencia", "Seleccione un producto primero"
            )
            return

        cantidad = self.cantidad_actual
        precio = self.producto_seleccionado.precio_venta
        subtotal = cantidad * precio

        item = {
            "nombre": self.producto_seleccionado.nombre,
            "cantidad": cantidad,
            "precio": precio,
            "subtotal": subtotal,
        }

        self.items_carrito.append(item)
        self._actualizar_carrito()
        self._limpiar_producto()
        logger.info(f"Producto agregado al carrito: {item['nombre']}")

    def _actualizar_carrito(self) -> None:
        """Actualizar visualización del carrito"""
        subtotal = sum(item["subtotal"] for item in self.items_carrito)
        self.ids.lbl_subtotal.text = f"{DEFAULT_CURRENCY}{subtotal:.2f}"
        self.ids.lbl_total.text = f"{DEFAULT_CURRENCY}{subtotal:.2f}"

    def _limpiar_producto(self) -> None:
        """Limpiar selección de producto"""
        self.producto_seleccionado = None
        self.producto_actual = "-"
        self.precio_actual = "-"
        self.stock_actual = "-"
        self.cantidad_actual = 1
        self.ids.txt_cantidad.text = "1"
        self.ids.txt_codigo.text = ""

    def limpiar_carrito(self) -> None:
        """Limpiar carrito"""
        self.items_carrito.clear()
        self._actualizar_carrito()
        logger.info("Carrito limpiado")

    def completar_venta(self) -> None:
        """Completar venta"""
        if not self.items_carrito:
            self._mostrar_alerta("Advertencia", "El carrito está vacío")
            return

        try:
            venta = self.gestor_ventas.crear_venta(
                vendedor_id=self.usuario_actual.id,
                cliente_nombre="Cliente Mobile",
                metodo_pago="efectivo",
            )

            self.gestor_ventas.completar_venta(venta.id)
            self._mostrar_alerta(
                "Éxito",
                f"Venta completada: {venta.numero_venta}",
            )
            self.limpiar_carrito()
            logger.info(f"Venta completada: {venta.numero_venta}")
        except Exception as e:
            logger.error(f"Error completando venta: {e}")
            self._mostrar_alerta("Error", f"Error en venta: {str(e)}")

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
