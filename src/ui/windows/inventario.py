"""Pantalla de inventario"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QSpinBox,
    QDoubleSpinBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from loguru import logger

from database.models import Producto
from logic.inventario import GestorInventario
from config.constants import DEFAULT_CURRENCY


class VentanaInventario(QWidget):
    """Ventana de gestión de inventario"""

    def __init__(self):
        """Inicializar ventana de inventario"""
        super().__init__()
        self.gestor_inventario = GestorInventario()
        self.setWindowTitle("Inventario - YeraPOV")
        self._crear_ui()
        self._cargar_productos()
        logger.info("Ventana de inventario creada")

    def _crear_ui(self) -> None:
        """Crear interfaz de usuario"""
        layout_principal = QVBoxLayout()

        # Título
        titulo = QLabel("Gestión de Inventario")
        titulo_font = QFont()
        titulo_font.setPointSize(14)
        titulo_font.setBold(True)
        titulo.setFont(titulo_font)
        layout_principal.addWidget(titulo)

        # Barra de herramientas
        layout_herramientas = QHBoxLayout()

        layout_herramientas.addWidget(QLabel("Búsqueda:"))
        self.txt_busqueda = QLineEdit()
        self.txt_busqueda.setPlaceholderText("Buscar por nombre o código...")
        self.txt_busqueda.textChanged.connect(self._filtrar_productos)
        layout_herramientas.addWidget(self.txt_busqueda)

        self.btn_nuevo = QPushButton("Nuevo Producto")
        self.btn_nuevo.clicked.connect(self._crear_nuevo_producto)
        layout_herramientas.addWidget(self.btn_nuevo)

        layout_principal.addLayout(layout_herramientas)

        # Tabla de productos
        self.tabla_productos = QTableWidget()
        self.tabla_productos.setColumnCount(8)
        self.tabla_productos.setHorizontalHeaderLabels(
            [
                "Código",
                "Nombre",
                "Categoría",
                "Precio Venta",
                "Stock Actual",
                "Stock Mín.",
                "Estado",
                "Acciones",
            ]
        )
        self.tabla_productos.setColumnWidth(0, 100)
        self.tabla_productos.setColumnWidth(1, 200)
        self.tabla_productos.setColumnWidth(2, 100)
        self.tabla_productos.setColumnWidth(3, 100)
        self.tabla_productos.setColumnWidth(4, 100)
        self.tabla_productos.setColumnWidth(5, 100)
        self.tabla_productos.setColumnWidth(6, 100)
        self.tabla_productos.setColumnWidth(7, 150)
        self.tabla_productos.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        layout_principal.addWidget(self.tabla_productos)

        self.setLayout(layout_principal)

    def _cargar_productos(self) -> None:
        """Cargar productos en tabla"""
        try:
            session = self.gestor_inventario.db.get_session()
            productos = (
                session.query(Producto).filter_by(activo=True).all()
            )
            session.close()

            self.tabla_productos.setRowCount(0)

            for idx, producto in enumerate(productos):
                self.tabla_productos.insertRow(idx)

                # Código
                self.tabla_productos.setItem(
                    idx, 0, QTableWidgetItem(producto.codigo_interno)
                )

                # Nombre
                self.tabla_productos.setItem(
                    idx, 1, QTableWidgetItem(producto.nombre)
                )

                # Categoría
                self.tabla_productos.setItem(
                    idx, 2, QTableWidgetItem(producto.categoria)
                )

                # Precio
                self.tabla_productos.setItem(
                    idx,
                    3,
                    QTableWidgetItem(
                        f"{DEFAULT_CURRENCY}{producto.precio_venta:.2f}"
                    ),
                )

                # Stock actual
                self.tabla_productos.setItem(
                    idx, 4, QTableWidgetItem(str(producto.stock_actual))
                )

                # Stock mínimo
                self.tabla_productos.setItem(
                    idx, 5, QTableWidgetItem(str(producto.stock_minimo))
                )

                # Estado (bajo stock?)
                if producto.stock_actual <= producto.stock_minimo:
                    item_estado = QTableWidgetItem("⚠️ Bajo Stock")
                    item_estado.setForeground(
                        Qt.GlobalColor.red
                    )  # type: ignore
                else:
                    item_estado = QTableWidgetItem("✓ OK")
                    item_estado.setForeground(
                        Qt.GlobalColor.green
                    )  # type: ignore

                self.tabla_productos.setItem(idx, 6, item_estado)

                # Botones de acción
                layout_acciones = QHBoxLayout()
                btn_editar = QPushButton("Editar")
                btn_editar.clicked.connect(
                    lambda checked, p=producto: self._editar_producto(p)
                )
                btn_stock = QPushButton("Stock")
                btn_stock.clicked.connect(
                    lambda checked, p=producto: self._ajustar_stock(p)
                )

                layout_acciones.addWidget(btn_editar)
                layout_acciones.addWidget(btn_stock)

                widget_acciones = QWidget()
                widget_acciones.setLayout(layout_acciones)
                self.tabla_productos.setCellWidget(idx, 7, widget_acciones)

        except Exception as e:
            logger.error(f"Error cargando productos: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Error cargando productos: {str(e)}",
            )

    def _filtrar_productos(self) -> None:
        """Filtrar productos por búsqueda"""
        busqueda = self.txt_busqueda.text().lower()

        for row in range(self.tabla_productos.rowCount()):
            # Obtener datos de la fila
            codigo = self.tabla_productos.item(row, 0)
            nombre = self.tabla_productos.item(row, 1)

            # Verificar si coincide
            coincide = (
                (codigo and busqueda in codigo.text().lower())
                or (nombre and busqueda in nombre.text().lower())
            )

            self.tabla_productos.setRowHidden(row, not coincide)

    def _crear_nuevo_producto(self) -> None:
        """Crear nuevo producto"""
        dialogo = DialogoProducto(self)
        if dialogo.exec() == QDialog.Accepted:
            try:
                self.gestor_inventario.crear_producto(
                    codigo_interno=dialogo.txt_codigo.text(),
                    nombre=dialogo.txt_nombre.text(),
                    categoria=dialogo.combo_categoria.currentText(),
                    precio_venta=float(dialogo.spin_precio.value()),
                    precio_costo=float(
                        dialogo.spin_costo.value()
                    ),
                    stock_inicial=dialogo.spin_stock.value(),
                    codigo_barras=dialogo.txt_barcode.text() or None,
                    stock_minimo=dialogo.spin_minimo.value(),
                )

                self._cargar_productos()
                QMessageBox.information(
                    self,
                    "Éxito",
                    "Producto creado exitosamente",
                )
            except Exception as e:
                logger.error(f"Error creando producto: {e}")
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Error creando producto: {str(e)}",
                )

    def _editar_producto(self, producto: Producto) -> None:
        """Editar producto"""
        QMessageBox.information(
            self,
            "En desarrollo",
            "La función de edición se implementará próximamente",
        )

    def _ajustar_stock(self, producto: Producto) -> None:
        """Ajustar stock de producto"""
        dialogo = DialogoAjusteStock(self, producto)
        if dialogo.exec() == QDialog.Accepted:
            try:
                self.gestor_inventario.actualizar_stock(
                    producto_id=producto.id,
                    cantidad=dialogo.spin_cantidad.value(),
                    tipo_movimiento=dialogo.combo_tipo.currentText().lower(),
                    razon=dialogo.txt_razon.text(),
                )

                self._cargar_productos()
                QMessageBox.information(
                    self,
                    "Éxito",
                    "Stock actualizado exitosamente",
                )
            except Exception as e:
                logger.error(f"Error actualizando stock: {e}")
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Error actualizando stock: {str(e)}",
                )


class DialogoProducto(QDialog):
    """Diálogo para crear/editar producto"""

    def __init__(self, parent=None):
        """Inicializar diálogo"""
        super().__init__(parent)
        self.setWindowTitle("Nuevo Producto")
        self.setGeometry(100, 100, 400, 350)
        self._crear_ui()

    def _crear_ui(self) -> None:
        """Crear interfaz"""
        layout = QFormLayout()

        self.txt_codigo = QLineEdit()
        layout.addRow("Código Interno:", self.txt_codigo)

        self.txt_nombre = QLineEdit()
        layout.addRow("Nombre:", self.txt_nombre)

        self.combo_categoria = QComboBox()
        self.combo_categoria.addItems(["General", "Alimentos", "Bebidas", "Otro"])
        layout.addRow("Categoría:", self.combo_categoria)

        self.spin_costo = QDoubleSpinBox()
        self.spin_costo.setRange(0, 9999)
        self.spin_costo.setDecimals(2)
        layout.addRow("Precio Costo:", self.spin_costo)

        self.spin_precio = QDoubleSpinBox()
        self.spin_precio.setRange(0, 9999)
        self.spin_precio.setDecimals(2)
        layout.addRow("Precio Venta:", self.spin_precio)

        self.spin_stock = QSpinBox()
        self.spin_stock.setRange(0, 99999)
        layout.addRow("Stock Inicial:", self.spin_stock)

        self.spin_minimo = QSpinBox()
        self.spin_minimo.setRange(1, 1000)
        self.spin_minimo.setValue(5)
        layout.addRow("Stock Mínimo:", self.spin_minimo)

        self.txt_barcode = QLineEdit()
        layout.addRow("Código de Barras:", self.txt_barcode)

        botones = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        botones.accepted.connect(self.accept)
        botones.rejected.connect(self.reject)
        layout.addRow(botones)

        self.setLayout(layout)


class DialogoAjusteStock(QDialog):
    """Diálogo para ajustar stock"""

    def __init__(self, parent=None, producto: Producto = None):
        """Inicializar diálogo"""
        super().__init__(parent)
        self.producto = producto
        self.setWindowTitle(f"Ajuste de Stock - {producto.nombre}")
        self.setGeometry(100, 100, 400, 200)
        self._crear_ui()

    def _crear_ui(self) -> None:
        """Crear interfaz"""
        layout = QFormLayout()

        layout.addRow(
            QLabel(
                f"Stock Actual: {self.producto.stock_actual} unidades"
            )
        )

        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Entrada", "Salida", "Ajuste", "Devolución"])
        layout.addRow("Tipo de Movimiento:", self.combo_tipo)

        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setRange(1, 99999)
        layout.addRow("Cantidad:", self.spin_cantidad)

        self.txt_razon = QLineEdit()
        self.txt_razon.setPlaceholderText("Motivo del movimiento")
        layout.addRow("Razón:", self.txt_razon)

        botones = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        botones.accepted.connect(self.accept)
        botones.rejected.connect(self.reject)
        layout.addRow(botones)

        self.setLayout(layout)
