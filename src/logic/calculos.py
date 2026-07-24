"""Módulo de cálculos automáticos de ventas"""

from typing import Dict, Tuple
from decimal import Decimal, ROUND_HALF_UP
from loguru import logger


class CalculosVenta:
    """Clase para realizar cálculos automáticos de ventas"""

    @staticmethod
    def calcular_vendido(inicio: float, entrada: float, final: float) -> float:
        """
        Cálculo automático: Inicio + Entrada = Venta; Venta - Final = Vendido
        
        Args:
            inicio: Stock inicial del producto
            entrada: Cantidad de compras/entradas
            final: Stock final actual
            
        Returns:
            Cantidad vendida (Vendido)
            
        Example:
            >>> CalculosVenta.calcular_vendido(1000, 500, 300)
            1200
        """
        try:
            venta = inicio + entrada
            vendido = venta - final
            
            if vendido < 0:
                logger.warning(f"Vendido negativo: {vendido}. Verificar datos.")
                return 0
            
            return vendido
        except Exception as e:
            logger.error(f"Error calculando vendido: {e}")
            raise

    @staticmethod
    def calcular_importe(vendido: float, precio: float) -> float:
        """
        Cálculo del importe: Vendido × Precio = Importe
        
        Args:
            vendido: Cantidad vendida
            precio: Precio unitario
            
        Returns:
            Importe total (Vendido × Precio)
            
        Example:
            >>> CalculosVenta.calcular_importe(1200, 10)
            12000
        """
        try:
            importe = Decimal(str(vendido)) * Decimal(str(precio))
            # Redondear a 2 decimales
            importe = importe.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            return float(importe)
        except Exception as e:
            logger.error(f"Error calculando importe: {e}")
            raise

    @staticmethod
    def calcular_venta_completa(
        inicio: float,
        entrada: float,
        final: float,
        precio: float,
    ) -> Dict[str, float]:
        """
        Cálculo completo de venta:
        - Venta = Inicio + Entrada
        - Vendido = Venta - Final
        - Importe = Vendido × Precio
        
        Args:
            inicio: Stock inicial
            entrada: Compras/entradas
            final: Stock final
            precio: Precio unitario
            
        Returns:
            Dict con:
            - venta: Stock disponible
            - vendido: Cantidad vendida
            - importe: Total de venta
        """
        try:
            venta = inicio + entrada
            vendido = CalculosVenta.calcular_vendido(inicio, entrada, final)
            importe = CalculosVenta.calcular_importe(vendido, precio)
            
            return {
                "inicio": inicio,
                "entrada": entrada,
                "venta": venta,
                "final": final,
                "vendido": vendido,
                "precio": precio,
                "importe": importe,
            }
        except Exception as e:
            logger.error(f"Error en cálculo completo de venta: {e}")
            raise

    @staticmethod
    def aplicar_descuento(monto: float, descuento_porcentaje: float = 0) -> float:
        """
        Aplicar descuento a un monto
        
        Args:
            monto: Monto original
            descuento_porcentaje: Porcentaje de descuento (0-100)
            
        Returns:
            Monto con descuento aplicado
        """
        try:
            if descuento_porcentaje < 0 or descuento_porcentaje > 100:
                logger.warning(f"Descuento fuera de rango: {descuento_porcentaje}%")
                return monto
            
            monto_decimal = Decimal(str(monto))
            descuento_decimal = Decimal(str(descuento_porcentaje)) / Decimal("100")
            monto_final = monto_decimal * (Decimal("1") - descuento_decimal)
            
            return float(monto_final.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
        except Exception as e:
            logger.error(f"Error aplicando descuento: {e}")
            raise

    @staticmethod
    def aplicar_impuesto(monto: float, porcentaje_impuesto: float = 0) -> Tuple[float, float]:
        """
        Calcular impuesto sobre un monto
        
        Args:
            monto: Monto base
            porcentaje_impuesto: Porcentaje de impuesto
            
        Returns:
            Tupla (monto_sin_impuesto, monto_impuesto, monto_total)
        """
        try:
            monto_decimal = Decimal(str(monto))
            impuesto_decimal = Decimal(str(porcentaje_impuesto)) / Decimal("100")
            monto_impuesto = monto_decimal * impuesto_decimal
            monto_total = monto_decimal + monto_impuesto
            
            return (
                float(monto_decimal),
                float(monto_impuesto.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
                float(monto_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
            )
        except Exception as e:
            logger.error(f"Error aplicando impuesto: {e}")
            raise

    @staticmethod
    def calcular_cambio(monto_pagado: float, monto_total: float) -> float:
        """
        Calcular cambio en una venta
        
        Args:
            monto_pagado: Monto pagado por el cliente
            monto_total: Total a pagar
            
        Returns:
            Cambio a devolver
        """
        try:
            cambio = Decimal(str(monto_pagado)) - Decimal(str(monto_total))
            
            if cambio < 0:
                logger.warning(f"Pago insuficiente. Falta: {abs(cambio)}")
                return 0
            
            return float(cambio.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
        except Exception as e:
            logger.error(f"Error calculando cambio: {e}")
            raise
