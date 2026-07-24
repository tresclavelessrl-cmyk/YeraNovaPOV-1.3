"""Generación de tickets de venta"""

from datetime import datetime
from typing import Optional, List
from loguru import logger
from decimal import Decimal

from database.models import Venta
from config.constants import TICKET_WIDTHS, DEFAULT_CURRENCY


class GeneradorTickets:
    """Generador de tickets de venta"""

    def __init__(self, ancho: int = 80):
        """
        Inicializar generador de tickets
        
        Args:
            ancho: Ancho del ticket en mm (58 o 80)
        """
        self.ancho = ancho
        self.caracteres_por_linea = self._calcular_caracteres_por_linea()
        logger.info(f"Generador de tickets inicializado (ancho: {ancho}mm)")

    def _calcular_caracteres_por_linea(self) -> int:
        """
        Calcular cantidad de caracteres por línea según ancho
        
        Returns:
            Número de caracteres
        """
        if self.ancho == 58:
            return 32  # Aproximado para 58mm
        elif self.ancho == 80:
            return 48  # Aproximado para 80mm
        else:
            return 40

    def generar_ticket(self, venta: Venta) -> str:
        """
        Generar ticket de venta en formato texto
        
        Args:
            venta: Objeto venta
            
        Returns:
            Texto formateado del ticket
        """
        try:
            lineas = []
            
            # Encabezado
            lineas.append(self._centrar("=" * self.caracteres_por_linea))
            lineas.append(self._centrar("YeraPOV - TICKET DE VENTA"))
            lineas.append(self._centrar("=" * self.caracteres_por_linea))
            lineas.append("")
            
            # Número de venta y fecha
            lineas.append(f"Venta: {venta.numero_venta}")
            lineas.append(f"Fecha: {venta.fecha_venta.strftime('%d/%m/%Y %H:%M:%S')}")
            if venta.vendedor:
                lineas.append(f"Vendedor: {venta.vendedor.nombre_completo}")
            lineas.append("")
            
            # Datos del cliente
            if venta.cliente_nombre:
                lineas.append(f"Cliente: {venta.cliente_nombre}")
            if venta.cliente_telefono:
                lineas.append(f"Teléfono: {venta.cliente_telefono}")
            lineas.append("")
            
            # Items
            lineas.append("-" * self.caracteres_por_linea)
            lineas.append(f"{'Item':<20} {'Cant':<6} {'Precio':<10}")
            lineas.append("-" * self.caracteres_por_linea)
            
            for detalle in venta.detalles:
                nombre_producto = detalle.producto.nombre[:20]
                cantidad = str(detalle.cantidad)
                subtotal = f"{DEFAULT_CURRENCY}{detalle.subtotal:.2f}"
                
                linea = f"{nombre_producto:<20} {cantidad:<6} {subtotal:<10}"
                lineas.append(linea)
            
            lineas.append("-" * self.caracteres_por_linea)
            
            # Totales
            lineas.append("")
            lineas.append(self._alinear_derecha(
                f"Subtotal: {DEFAULT_CURRENCY}{venta.subtotal:.2f}"
            ))
            
            if venta.descuento > 0:
                lineas.append(self._alinear_derecha(
                    f"Descuento: -{DEFAULT_CURRENCY}{venta.descuento:.2f}"
                ))
            
            if venta.impuesto > 0:
                lineas.append(self._alinear_derecha(
                    f"Impuesto: {DEFAULT_CURRENCY}{venta.impuesto:.2f}"
                ))
            
            lineas.append(self._alinear_derecha(
                f"TOTAL: {DEFAULT_CURRENCY}{venta.total:.2f}",
                negrita=True
            ))
            
            # Footer
            lineas.append("")
            lineas.append("-" * self.caracteres_por_linea)
            lineas.append(self._centrar("Gracias por su compra"))
            lineas.append(self._centrar(datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
            lineas.append("=" * self.caracteres_por_linea)
            
            return "\n".join(lineas)
            
        except Exception as e:
            logger.error(f"Error generando ticket: {e}")
            raise

    def _centrar(self, texto: str, negrita: bool = False) -> str:
        """
        Centrar texto en el ticket
        
        Args:
            texto: Texto a centrar
            negrita: Si es True, agrega asteriscos
            
        Returns:
            Texto centrado
        """
        espacios_faltantes = self.caracteres_por_linea - len(texto)
        izq = espacios_faltantes // 2
        der = espacios_faltantes - izq
        
        if negrita:
            return " " * izq + f"*{texto}*" + " " * der
        return " " * izq + texto + " " * der

    def _alinear_derecha(self, texto: str, negrita: bool = False) -> str:
        """
        Alinear texto a la derecha
        
        Args:
            texto: Texto a alinear
            negrita: Si es True, agrega asteriscos
            
        Returns:
            Texto alineado a derecha
        """
        espacios_faltantes = self.caracteres_por_linea - len(texto)
        
        if negrita:
            return " " * espacios_faltantes + f"*{texto}*"
        return " " * espacios_faltantes + texto

    def guardar_ticket(self, venta: Venta, ruta_salida: str) -> bool:
        """
        Guardar ticket en archivo
        
        Args:
            venta: Objeto venta
            ruta_salida: Ruta donde guardar el ticket
            
        Returns:
            True si se guardó exitosamente
        """
        try:
            ticket_texto = self.generar_ticket(venta)
            
            with open(ruta_salida, "w", encoding="utf-8") as f:
                f.write(ticket_texto)
            
            logger.info(f"Ticket guardado: {ruta_salida}")
            return True
            
        except Exception as e:
            logger.error(f"Error guardando ticket: {e}")
            return False
