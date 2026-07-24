"""Exportación de datos a Excel"""

from typing import List, Optional
from datetime import datetime
from loguru import logger

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter


class ExcelExporter:
    """Exportador de datos a formato Excel"""

    def __init__(self):
        """Inicializar exportador de Excel"""
        logger.info("Exportador de Excel inicializado")

    @staticmethod
    def exportar_ventas(
        ruta_salida: str,
        ventas: List,
        incluir_detalles: bool = True,
    ) -> bool:
        """
        Exportar ventas a Excel
        
        Args:
            ruta_salida: Ruta del archivo Excel
            ventas: Lista de ventas
            incluir_detalles: Si True, incluye detalles de cada venta
            
        Returns:
            True si se exportó exitosamente
        """
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Ventas"
            
            # Encabezados
            encabezados = [
                "N° Venta",
                "Fecha",
                "Vendedor",
                "Cliente",
                "Teléfono",
                "Subtotal",
                "Descuento",
                "Impuesto",
                "Total",
                "Método Pago",
                "Estado",
            ]
            
            # Dar formato a encabezados
            header_fill = PatternFill(start_color="1f4788", end_color="1f4788", fill_type="solid")
            header_font = Font(bold=True, color="FFFFFF")
            
            for col_num, encabezado in enumerate(encabezados, 1):
                cell = ws.cell(row=1, column=col_num)
                cell.value = encabezado
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center")
            
            # Datos
            for row_num, venta in enumerate(ventas, 2):
                ws.cell(row=row_num, column=1).value = venta.numero_venta
                ws.cell(row=row_num, column=2).value = venta.fecha_venta.strftime("%d/%m/%Y %H:%M")
                ws.cell(row=row_num, column=3).value = venta.vendedor.nombre_completo if venta.vendedor else "-"
                ws.cell(row=row_num, column=4).value = venta.cliente_nombre or "-"
                ws.cell(row=row_num, column=5).value = venta.cliente_telefono or "-"
                ws.cell(row=row_num, column=6).value = venta.subtotal
                ws.cell(row=row_num, column=7).value = venta.descuento
                ws.cell(row=row_num, column=8).value = venta.impuesto
                ws.cell(row=row_num, column=9).value = venta.total
                ws.cell(row=row_num, column=10).value = venta.metodo_pago or "-"
                ws.cell(row=row_num, column=11).value = venta.estado.value if venta.estado else "-"
            
            # Ajustar ancho de columnas
            for column in ws.columns:
                max_length = 0
                column_letter = get_column_letter(column[0].column)
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column_letter].width = adjusted_width
            
            # Guardar
            wb.save(ruta_salida)
            logger.info(f"Ventas exportadas a Excel: {ruta_salida}")
            return True
            
        except Exception as e:
            logger.error(f"Error exportando a Excel: {e}")
            return False

    @staticmethod
    def exportar_inventario(
        ruta_salida: str,
        productos: List,
    ) -> bool:
        """
        Exportar inventario a Excel
        
        Args:
            ruta_salida: Ruta del archivo Excel
            productos: Lista de productos
            
        Returns:
            True si se exportó exitosamente
        """
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Inventario"
            
            # Encabezados
            encabezados = [
                "Código Interno",
                "Código Barras",
                "Nombre",
                "Categoría",
                "Precio Costo",
                "Precio Venta",
                "Stock Inicial",
                "Stock Actual",
                "Stock Mínimo",
                "Descripción",
            ]
            
            # Dar formato a encabezados
            header_fill = PatternFill(start_color="1f4788", end_color="1f4788", fill_type="solid")
            header_font = Font(bold=True, color="FFFFFF")
            
            for col_num, encabezado in enumerate(encabezados, 1):
                cell = ws.cell(row=1, column=col_num)
                cell.value = encabezado
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center")
            
            # Datos
            for row_num, producto in enumerate(productos, 2):
                ws.cell(row=row_num, column=1).value = producto.codigo_interno
                ws.cell(row=row_num, column=2).value = producto.codigo_barras or "-"
                ws.cell(row=row_num, column=3).value = producto.nombre
                ws.cell(row=row_num, column=4).value = producto.categoria
                ws.cell(row=row_num, column=5).value = producto.precio_costo
                ws.cell(row=row_num, column=6).value = producto.precio_venta
                ws.cell(row=row_num, column=7).value = producto.stock_inicial
                ws.cell(row=row_num, column=8).value = producto.stock_actual
                ws.cell(row=row_num, column=9).value = producto.stock_minimo
                ws.cell(row=row_num, column=10).value = producto.descripcion or "-"
            
            # Ajustar ancho de columnas
            for column in ws.columns:
                max_length = 0
                column_letter = get_column_letter(column[0].column)
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column_letter].width = adjusted_width
            
            # Guardar
            wb.save(ruta_salida)
            logger.info(f"Inventario exportado a Excel: {ruta_salida}")
            return True
            
        except Exception as e:
            logger.error(f"Error exportando inventario a Excel: {e}")
            return False
