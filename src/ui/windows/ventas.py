"""Pantalla de ventas"""

from datetime import datetime
from typing import Optional, List
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QSpinBox,
    QDoubleSpinBox,
    QMessageBox,
    QComboBox,
    QGroupBox,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor
from loguru import logger

from database.models import Venta, DetalleVenta, Producto, Usuario
from logic.ventas import GestorVentas
from logic.inventario import GestorInventario
from logic.calculos import CalculosVenta
from config.constants import DEFAULT_CURRENCY


class VentanaVentas(QWidget):
    """Ventana de ventas"""

    def __init__(self, usuario_actual: Usuario):
        """Inicializar ventana de ventas"""
        super().__init__()
        self.usuario_actual = usuario_actual
        self.gestor_ventas = GestorVentas()
        self.gestor_inventario = GestorInventario()
        self.venta_actual: Optional[Venta] = None
        self.items_carrito: List[dict] = []

        self.setWindowTitle("Ventas - YeraPOV")
        self._crear_ui()
        logger.info("Ventana de ventas creada")

    def _crear_ui(self) -> None:
        """Crear interfaz de usuario"""
        layout_principal = QHBoxLayout()

        # Panel izquierdo - Entrada de producto
        layout_izquierdo = QVBoxLayout()

        # Título
        titulo = QLabel("Nueva Venta")
        titulo_font = QFont()
        titulo_font.setPointSize(14)
        titulo_font.setBold(True)
        titulo.setFont(titulo_font)
        layout_izquierdo.addWidget(titulo)

        # Código de barras / Búsqueda
        layout_codigo = QHBoxLayout()
        layout_codigo.addWidget(QLabel("Código/Producto:"))
        self.txt_codigo = QLineEdit()
        self.txt_codigo.setPlaceholderText("Escanee código o escriba nombre")
        self.txt_codigo.returnPressed.connect(self._buscar_producto)
        layout_codigo.addWidget(self.txt_codigo)
        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self._buscar_producto)
        layout_codigo.addWidget(self.btn_buscar)
        layout_izquierdo.addLayout(layout_codigo)

        # Información del producto
        grupo_producto = QGroupBox("Información del Producto")
        layout_producto = QVBoxLayout()

        layout_nombre = QHBoxLayout()
        layout_nombre.addWidget(QLabel("Nombre:"))
        self.lbl_nombre = QLabel("-")
        layout_nombre.addWidget(self.lbl_nombre)
        layout_producto.addLayout(layout_nombre)

        layout_precio = QHBoxLayout()
        layout_precio.addWidget(QLabel("Precio:"))
        self.lbl_precio = QLabel("-")
        layout_precio.addWidget(self.lbl_precio)
        layout_precio.addStretch()
        layout_producto.addLayout(layout_precio)

        layout_stock = QHBoxLayout()
        layout_stock.addWidget(QLabel("Stock:"))
        self.lbl_stock = QLabel("-")
        layout_stock.addWidget(self.lbl_stock)
        layout_stock.addStretch()
        layout_producto.addLayout(layout_stock)

        grupo_producto.setLayout(layout_producto)
        layout_izquierdo.addWidget(grupo_producto)

        # Cantidad
        layout_cantidad = QHBoxLayout()
        layout_cantidad.addWidget(QLabel("Cantidad:"))
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(1)
        self.spin_cantidad.setMaximum(9999)
        self.spin_cantidad.setValue(1)
        layout_cantidad.addWidget(self.spin_cantidad)
        layout_cantidad.addStretch()
        layout_izquierdo.addLayout(layout_cantidad)

        # Botón agregar al carrito
        self.btn_agregar = QPushButton("Agregar al Carrito")
        self.btn_agregar.setMinimumHeight(35)
        self.btn_agregar.clicked.connect(self._agregar_al_carrito)
        layout_izquierdo.addWidget(self.btn_agregar)

        layout_izquierdo.addSpacing(20)

        # Datos del cliente
        grupo_cliente = QGroupBox("Datos del Cliente")
        layout_cliente = QVBoxLayout()

        layout_cliente_nombre = QHBoxLayout()
        layout_cliente_nombre.addWidget(QLabel("Nombre:"))
        self.txt_cliente_nombre = QLineEdit()
        layout_cliente_nombre.addWidget(self.txt_cliente_nombre)
        layout_cliente.addLayout(layout_cliente_nombre)

        layout_cliente_tel = QHBoxLayout()
        layout_cliente_tel.addWidget(QLabel("Teléfono:"))
        self.txt_cliente_tel = QLineEdit()
        layout_cliente_tel.addWidget(self.txt_cliente_tel)
        layout_cliente.addLayout(layout_cliente_tel)

        grupo_cliente.setLayout(layout_cliente)
        layout_izquierdo.addWidget(grupo_cliente)

        # Método de pago
        layout_pago = QHBoxLayout()
        layout_pago.addWidget(QLabel("Método de Pago:"))
        self.combo_metodo_pago = QComboBox()
        self.combo_metodo_pago.addItems([
            "Efectivo",
            "Tarjeta Débito",
            "Tarjeta Crédito",
            "Transferencia",
            "Cheque",
        ])
        layout_pago.addWidget(self.combo_metodo_pago)
        layout_pago.addStretch()
        layout_izquierdo.addLayout(layout_pago)

        layout_izquierdo.addStretch()

        # Panel derecho - Carrito
        layout_derecho = QVBoxLayout()

        titulo_carrito = QLabel("Carrito de Compras")
        titulo_carrito_font = QFont()
        titulo_carrito_font.setPointSize(12)
        titulo_carrito_font.setBold(True)
        titulo_carrito.setFont(titulo_carrito_font)
        layout_derecho.addWidget(titulo_carrito)

        # Tabla de carrito
        self.tabla_carrito = QTableWidget()
        self.tabla_carrito.setColumnCount(6)
        self.tabla_carrito.setHorizontalHeaderLabels(
            ["Producto", "Cantidad", "Precio", "Descuento", "Subtotal", ""]
        )
        self.tabla_carrito.setColumnWidth(0, 150)
        self.tabla_carrito.setColumnWidth(1, 80)
        self.tabla_carrito.setColumnWidth(2, 80)
        self.tabla_carrito.setColumnWidth(3, 80)
        self.tabla_carrito.setColumnWidth(4, 100)
        layout_derecho.addWidget(self.tabla_carrito)

        # Totales
        grupo_totales = QGroupBox("Totales")
        layout_totales = QVBoxLayout()

        layout_subtotal = QHBoxLayout()
        layout_subtotal.addWidget(QLabel("Subtotal:"))
        self.lbl_subtotal = QLabel(f"{DEFAULT_CURRENCY}0.00")
        lbl_subtotal_font = QFont()
        lbl_subtotal_font.setPointSize(11)
        lbl_subtotal_font.setBold(True)
        self.lbl_subtotal.setFont(lbl_subtotal_font)
        layout_subtotal.addStretch()
        layout_subtotal.addWidget(self.lbl_subtotal)
        layout_totales.addLayout(layout_subtotal)

        layout_descuento = QHBoxLayout()
        layout_descuento.addWidget(QLabel("Descuento:"))
        self.spin_descuento = QDoubleSpinBox()
        self.spin_descuento.setRange(0, 100)
        self.spin_descuento.setSuffix("%")
        self.spin_descuento.valueChanged.connect(self._recalcular_totales)
        layout_descuento.addStretch()
        layout_descuento.addWidget(self.spin_descuento)
        layout_totales.addLayout(layout_descuento)

        layout_total = QHBoxLayout()
        layout_total.addWidget(QLabel("TOTAL:"))
        self.lbl_total = QLabel(f"{DEFAULT_CURRENCY}0.00")
        lbl_total_font = QFont()
        lbl_total_font.setPointSize(14)
        lbl_total_font.setBold(True)
        self.lbl_total.setFont(lbl_total_font)
        self.lbl_total.setStyleSheet("color: #1f4788;")
        layout_total.addStretch()
        layout_total.addWidget(self.lbl_total)
        layout_totales.addLayout(layout_total)

        grupo_totales.setLayout(layout_totales)
        layout_derecho.addWidget(grupo_totales)

        # Botones de acción
        layout_botones = QHBoxLayout()

        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_limpiar.clicked.connect(self._limpiar_carrito)
        layout_botones.addWidget(self.btn_limpiar)

        self.btn_completar = QPushButton("Completar Venta")
        self.btn_completar.setMinimumHeight(40)
        self.btn_completar.setStyleSheet("background-color: #4CAF50;")
        self.btn_completar.clicked.connect(self._completar_venta)
        layout_botones.addWidget(self.btn_completar)

        layout_derecho.addLayout(layout_botones)

        # Agregar paneles al layout principal
        layout_principal.addLayout(layout_izquierdo, 1)
        layout_principal.addLayout(layout_derecho, 1)

        self.setLayout(layout_principal)

    def _buscar_producto(self) -> None:
        """Buscar producto por código o nombre"""
        codigo = self.txt_codigo.text().strip()

        if not codigo:
            QMessageBox.warning(self, "Advertencia", "Ingrese un código de barras")
            return

        # Buscar por código de barras
        producto = self.gestor_inventario.obtener_producto_por_codigo_barras(codigo)

        if producto:
            self._mostrar_producto(producto)
            self.spin_cantidad.setFocus()
        else:
            QMessageBox.warning(
                self,
                "Producto no encontrado",
                f"No se encontró producto con código: {codigo}",
            )
            self.txt_codigo.clear()
            self.txt_codigo.setFocus()

    def _mostrar_producto(self, producto: Producto) -> None:
        """Mostrar información del producto"""
        self.lbl_nombre.setText(producto.nombre)
        self.lbl_precio.setText(f"{DEFAULT_CURRENCY}{producto.precio_venta:.2f}")
        self.lbl_stock.setText(f"{producto.stock_actual} unidades")
        self.spin_cantidad.setMaximum(max(producto.stock_actual, 1))

    def _agregar_al_carrito(self) -> None:
        """Agregar producto al carrito"""
        nombre_producto = self.lbl_nombre.text()

        if nombre_producto == "-":
            QMessageBox.warning(self, "Advertencia", "Seleccione un producto primero")
            return

        cantidad = self.spin_cantidad.value()
        precio = float(self.lbl_precio.text().replace(DEFAULT_CURRENCY, ""))

        # Calcular subtotal
        subtotal = cantidad * precio

        # Agregar a carrito
        item = {
            "nombre": nombre_producto,
            "cantidad": cantidad,
            "precio": precio,
            "subtotal": subtotal,
        }

        self.items_carrito.append(item)
        self._actualizar_tabla_carrito()
        self._recalcular_totales()

        # Limpiar
        self.txt_codigo.clear()
        self.lbl_nombre.setText("-")
        self.lbl_precio.setText("-")
        self.lbl_stock.setText("-")
        self.spin_cantidad.setValue(1)
        self.txt_codigo.setFocus()

    def _actualizar_tabla_carrito(self) -> None:
        """Actualizar tabla de carrito"""
        self.tabla_carrito.setRowCount(0)

        for idx, item in enumerate(self.items_carrito):
            self.tabla_carrito.insertRow(idx)

            # Nombre
            self.tabla_carrito.setItem(idx, 0, QTableWidgetItem(item["nombre"]))

            # Cantidad
            self.tabla_carrito.setItem(
                idx, 1, QTableWidgetItem(str(item["cantidad"]))
            )

            # Precio
            self.tabla_carrito.setItem(
                idx, 2, QTableWidgetItem(f"{DEFAULT_CURRENCY}{item['precio']:.2f}")
            )

            # Descuento
            self.tabla_carrito.setItem(idx, 3, QTableWidgetItem("-"))

            # Subtotal
            self.tabla_carrito.setItem(
                idx,
                4,
                QTableWidgetItem(f"{DEFAULT_CURRENCY}{item['subtotal']:.2f}"),
            )

            # Botón eliminar
            btn_eliminar = QPushButton("X")
            btn_eliminar.setMaximumWidth(30)
            btn_eliminar.clicked.connect(lambda checked, i=idx: self._eliminar_del_carrito(i))
            self.tabla_carrito.setCellWidget(idx, 5, btn_eliminar)

    def _eliminar_del_carrito(self, index: int) -> None:
        """Eliminar item del carrito"""
        if 0 <= index < len(self.items_carrito):
            self.items_carrito.pop(index)
            self._actualizar_tabla_carrito()
            self._recalcular_totales()

    def _recalcular_totales(self) -> None:
        """Recalcular totales"""
        subtotal = sum(item["subtotal"] for item in self.items_carrito)

        descuento_porcentaje = self.spin_descuento.value()
        descuento_monto = CalculosVenta.aplicar_descuento(
            subtotal, -descuento_porcentaje
        )
        descuento_aplicado = subtotal - descuento_monto

        total = subtotal - descuento_aplicado

        self.lbl_subtotal.setText(f"{DEFAULT_CURRENCY}{subtotal:.2f}")
        self.lbl_total.setText(f"{DEFAULT_CURRENCY}{total:.2f}")

    def _limpiar_carrito(self) -> None:
        """Limpiar carrito"""
        respuesta = QMessageBox.question(
            self,
            "Confirmar",
            "¿Está seguro de que desea limpiar el carrito?",
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            self.items_carrito.clear()
            self._actualizar_tabla_carrito()
            self._recalcular_totales()
            self.txt_codigo.setFocus()

    def _completar_venta(self) -> None:
        """Completar venta"""
        if not self.items_carrito:
            QMessageBox.warning(self, "Advertencia", "El carrito está vacío")
            return

        try:
            # Crear venta
            venta = self.gestor_ventas.crear_venta(
                vendedor_id=self.usuario_actual.id,
                cliente_nombre=self.txt_cliente_nombre.text() or "Cliente Genérico",
                cliente_telefono=self.txt_cliente_tel.text() or None,
                metodo_pago=self.combo_metodo_pago.currentText().lower(),
            )

            # Completar venta
            self.gestor_ventas.completar_venta(venta.id)

            QMessageBox.information(
                self,
                "Éxito",
                f"Venta completada: {venta.numero_venta}\nTotal: {DEFAULT_CURRENCY}{venta.total:.2f}",
            )

            # Limpiar
            self._limpiar_formulario()

        except Exception as e:
            logger.error(f"Error completando venta: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Error completando venta: {str(e)}",
            )

    def _limpiar_formulario(self) -> None:
        """Limpiar formulario completo"""
        self.items_carrito.clear()
        self._actualizar_tabla_carrito()
        self._recalcular_totales()
        self.txt_cliente_nombre.clear()
        self.txt_cliente_tel.clear()
        self.spin_descuento.setValue(0)
        self.txt_codigo.clear()
        self.txt_codigo.setFocus()
