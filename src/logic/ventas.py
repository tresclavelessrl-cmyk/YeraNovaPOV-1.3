"""Gestor de ventas"""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from decimal import Decimal
from loguru import logger
from sqlalchemy.orm import Session

from database.models import Venta, DetalleVenta, Producto, Inventario
from database.connection import get_db
from config.constants import ESTADO_VENTA
from .calculos import CalculosVenta


class GestorVentas:
    """Clase para gestionar ventas"""

    def __init__(self):
        """Inicializar gestor de ventas"""
        self.db = get_db()
        logger.info("Gestor de ventas inicializado")

    def crear_venta(
        self,
        vendedor_id: int,
        cliente_nombre: Optional[str] = None,
        cliente_telefono: Optional[str] = None,
        cliente_email: Optional[str] = None,
        metodo_pago: str = "efectivo",
        descuento: float = 0,
        impuesto: float = 0,
        nota: Optional[str] = None,
    ) -> Venta:
        """
        Crear nueva venta
        
        Args:
            vendedor_id: ID del vendedor
            cliente_nombre: Nombre del cliente
            cliente_telefono: Teléfono del cliente
            cliente_email: Email del cliente
            metodo_pago: Método de pago
            descuento: Descuento en porcentaje
            impuesto: Impuesto en porcentaje
            nota: Notas de la venta
            
        Returns:
            Objeto Venta creado
        """
        try:
            session = self.db.get_session()
            
            # Generar número de venta único
            numero_venta = f"VEN{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            venta = Venta(
                numero_venta=numero_venta,
                fecha_venta=datetime.now(),
                vendedor_id=vendedor_id,
                cliente_nombre=cliente_nombre,
                cliente_telefono=cliente_telefono,
                cliente_email=cliente_email,
                estado=ESTADO_VENTA.PENDIENTE,
                metodo_pago=metodo_pago,
                nota=nota,
            )
            
            session.add(venta)
            session.commit()
            
            logger.info(f"Venta creada: {numero_venta}")
            return venta
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error creando venta: {e}")
            raise
        finally:
            session.close()

    def agregar_item_venta(
        self,
        venta_id: int,
        producto_id: int,
        cantidad: int,
        descuento_linea: float = 0,
    ) -> DetalleVenta:
        """
        Agregar item a una venta
        
        Args:
            venta_id: ID de la venta
            producto_id: ID del producto
            cantidad: Cantidad vendida
            descuento_linea: Descuento de la línea
            
        Returns:
            DetalleVenta creado
        """
        try:
            session = self.db.get_session()
            
            # Obtener producto
            producto = session.query(Producto).filter_by(id=producto_id).first()
            if not producto:
                raise ValueError(f"Producto {producto_id} no existe")
            
            # Validar stock
            if producto.stock_actual < cantidad:
                raise ValueError(
                    f"Stock insuficiente. Disponible: {producto.stock_actual}, "
                    f"Solicitado: {cantidad}"
                )
            
            # Calcular subtotal
            subtotal = producto.precio_venta * cantidad
            subtotal = CalculosVenta.aplicar_descuento(subtotal, descuento_linea)
            
            # Crear detalle
            detalle = DetalleVenta(
                venta_id=venta_id,
                producto_id=producto_id,
                cantidad=cantidad,
                precio_unitario=producto.precio_venta,
                descuento_linea=descuento_linea,
                subtotal=subtotal,
            )
            
            session.add(detalle)
            
            # Actualizar totales de venta
            venta = session.query(Venta).filter_by(id=venta_id).first()
            if venta:
                venta.subtotal += subtotal
                venta.total = venta.subtotal + venta.impuesto - venta.descuento
            
            session.commit()
            logger.info(f"Item agregado a venta {venta_id}")
            return detalle
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error agregando item a venta: {e}")
            raise
        finally:
            session.close()

    def completar_venta(self, venta_id: int) -> Venta:
        """
        Completar una venta (marcarla como completada y actualizar inventario)
        
        Args:
            venta_id: ID de la venta
            
        Returns:
            Venta completada
        """
        try:
            session = self.db.get_session()
            
            venta = session.query(Venta).filter_by(id=venta_id).first()
            if not venta:
                raise ValueError(f"Venta {venta_id} no existe")
            
            # Procesar cada item de la venta
            for detalle in venta.detalles:
                producto = detalle.producto
                
                # Actualizar stock
                stock_anterior = producto.stock_actual
                producto.stock_actual -= detalle.cantidad
                
                # Registrar movimiento de inventario
                movimiento = Inventario(
                    producto_id=producto.id,
                    tipo_movimiento="salida",
                    cantidad=detalle.cantidad,
                    stock_anterior=stock_anterior,
                    stock_nuevo=producto.stock_actual,
                    razon="Venta",
                    referencia=venta.numero_venta,
                    fecha=datetime.now(),
                )
                session.add(movimiento)
            
            # Marcar venta como completada
            venta.estado = ESTADO_VENTA.COMPLETADA
            venta.fecha_venta = datetime.now()
            
            session.commit()
            logger.info(f"Venta {venta_id} completada")
            return venta
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error completando venta: {e}")
            raise
        finally:
            session.close()

    def cancelar_venta(self, venta_id: int, razon: Optional[str] = None) -> Venta:
        """
        Cancelar una venta
        
        Args:
            venta_id: ID de la venta
            razon: Razón de la cancelación
            
        Returns:
            Venta cancelada
        """
        try:
            session = self.db.get_session()
            
            venta = session.query(Venta).filter_by(id=venta_id).first()
            if not venta:
                raise ValueError(f"Venta {venta_id} no existe")
            
            venta.estado = ESTADO_VENTA.CANCELADA
            if razon:
                venta.nota = f"Cancelada: {razon}"
            
            session.commit()
            logger.info(f"Venta {venta_id} cancelada")
            return venta
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error cancelando venta: {e}")
            raise
        finally:
            session.close()

    def obtener_venta(self, venta_id: int) -> Optional[Venta]:
        """
        Obtener detalles de una venta
        
        Args:
            venta_id: ID de la venta
            
        Returns:
            Objeto Venta o None
        """
        try:
            session = self.db.get_session()
            venta = session.query(Venta).filter_by(id=venta_id).first()
            return venta
        except Exception as e:
            logger.error(f"Error obteniendo venta: {e}")
            raise
        finally:
            session.close()

    def obtener_ventas_por_fecha(
        self,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        vendedor_id: Optional[int] = None,
    ) -> List[Venta]:
        """
        Obtener ventas en un rango de fechas
        
        Args:
            fecha_inicio: Fecha inicio
            fecha_fin: Fecha fin
            vendedor_id: Filtrar por vendedor (opcional)
            
        Returns:
            Lista de ventas
        """
        try:
            session = self.db.get_session()
            
            query = session.query(Venta).filter(
                Venta.fecha_venta >= fecha_inicio,
                Venta.fecha_venta <= fecha_fin,
            )
            
            if vendedor_id:
                query = query.filter_by(vendedor_id=vendedor_id)
            
            ventas = query.order_by(Venta.fecha_venta.desc()).all()
            return ventas
            
        except Exception as e:
            logger.error(f"Error obteniendo ventas por fecha: {e}")
            raise
        finally:
            session.close()
