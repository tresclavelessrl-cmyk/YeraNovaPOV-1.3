"""Gestor de inventario"""

from datetime import datetime
from typing import List, Optional, Dict
from loguru import logger
from sqlalchemy.orm import Session

from database.models import Producto, Inventario
from database.connection import get_db


class GestorInventario:
    """Clase para gestionar inventario"""

    def __init__(self):
        """Inicializar gestor de inventario"""
        self.db = get_db()
        logger.info("Gestor de inventario inicializado")

    def crear_producto(
        self,
        codigo_interno: str,
        nombre: str,
        categoria: str,
        precio_venta: float,
        stock_inicial: int = 0,
        precio_costo: Optional[float] = None,
        codigo_barras: Optional[str] = None,
        descripcion: Optional[str] = None,
        stock_minimo: int = 5,
    ) -> Producto:
        """
        Crear nuevo producto
        
        Args:
            codigo_interno: Código interno del producto
            nombre: Nombre del producto
            categoria: Categoría
            precio_venta: Precio de venta
            stock_inicial: Stock inicial
            precio_costo: Precio de costo
            codigo_barras: Código de barras
            descripcion: Descripción
            stock_minimo: Stock mínimo
            
        Returns:
            Producto creado
        """
        try:
            session = self.db.get_session()
            
            # Validar que el código interno sea único
            existente = session.query(Producto).filter_by(
                codigo_interno=codigo_interno
            ).first()
            if existente:
                raise ValueError(f"Código interno {codigo_interno} ya existe")
            
            producto = Producto(
                codigo_interno=codigo_interno,
                nombre=nombre,
                categoria=categoria,
                precio_venta=precio_venta,
                stock_inicial=stock_inicial,
                stock_actual=stock_inicial,
                precio_costo=precio_costo or precio_venta,
                codigo_barras=codigo_barras,
                descripcion=descripcion,
                stock_minimo=stock_minimo,
            )
            
            session.add(producto)
            session.commit()
            
            logger.info(f"Producto creado: {nombre}")
            return producto
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error creando producto: {e}")
            raise
        finally:
            session.close()

    def actualizar_stock(
        self,
        producto_id: int,
        cantidad: int,
        tipo_movimiento: str,
        razon: Optional[str] = None,
        referencia: Optional[str] = None,
    ) -> Inventario:
        """
        Actualizar stock de un producto
        
        Args:
            producto_id: ID del producto
            cantidad: Cantidad a sumar/restar
            tipo_movimiento: entrada, salida, ajuste, devolucion
            razon: Razón del movimiento
            referencia: Referencia (nº venta, nº compra, etc)
            
        Returns:
            Movimiento de inventario
        """
        try:
            session = self.db.get_session()
            
            # Obtener producto
            producto = session.query(Producto).filter_by(id=producto_id).first()
            if not producto:
                raise ValueError(f"Producto {producto_id} no existe")
            
            # Calcular nuevo stock
            stock_anterior = producto.stock_actual
            
            if tipo_movimiento == "entrada":
                stock_nuevo = stock_anterior + cantidad
            elif tipo_movimiento == "salida":
                stock_nuevo = stock_anterior - cantidad
                if stock_nuevo < 0:
                    raise ValueError(f"Stock insuficiente para salida")
            elif tipo_movimiento == "ajuste":
                stock_nuevo = cantidad  # Ajuste establece el valor
            elif tipo_movimiento == "devolucion":
                stock_nuevo = stock_anterior + cantidad
            else:
                raise ValueError(f"Tipo de movimiento inválido: {tipo_movimiento}")
            
            # Actualizar producto
            producto.stock_actual = stock_nuevo
            
            # Crear movimiento de inventario
            movimiento = Inventario(
                producto_id=producto_id,
                tipo_movimiento=tipo_movimiento,
                cantidad=cantidad,
                stock_anterior=stock_anterior,
                stock_nuevo=stock_nuevo,
                razon=razon,
                referencia=referencia,
                fecha=datetime.now(),
            )
            
            session.add(movimiento)
            session.commit()
            
            logger.info(
                f"Stock actualizado: {producto.nombre} "
                f"{stock_anterior} -> {stock_nuevo}"
            )
            return movimiento
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error actualizando stock: {e}")
            raise
        finally:
            session.close()

    def obtener_productos_con_bajo_stock(self) -> List[Producto]:
        """
        Obtener productos con stock por debajo del mínimo
        
        Returns:
            Lista de productos
        """
        try:
            session = self.db.get_session()
            
            productos = session.query(Producto).filter(
                Producto.stock_actual <= Producto.stock_minimo,
                Producto.activo == True,
            ).all()
            
            return productos
            
        except Exception as e:
            logger.error(f"Error obteniendo productos con bajo stock: {e}")
            raise
        finally:
            session.close()

    def obtener_producto_por_codigo_barras(
        self, codigo_barras: str
    ) -> Optional[Producto]:
        """
        Obtener producto por código de barras
        
        Args:
            codigo_barras: Código de barras
            
        Returns:
            Producto o None
        """
        try:
            session = self.db.get_session()
            
            producto = session.query(Producto).filter_by(
                codigo_barras=codigo_barras,
                activo=True,
            ).first()
            
            return producto
            
        except Exception as e:
            logger.error(f"Error buscando producto por código de barras: {e}")
            raise
        finally:
            session.close()

    def obtener_productos_por_categoria(self, categoria: str) -> List[Producto]:
        """
        Obtener productos por categoría
        
        Args:
            categoria: Categoría
            
        Returns:
            Lista de productos
        """
        try:
            session = self.db.get_session()
            
            productos = session.query(Producto).filter_by(
                categoria=categoria,
                activo=True,
            ).order_by(Producto.nombre).all()
            
            return productos
            
        except Exception as e:
            logger.error(f"Error obteniendo productos por categoría: {e}")
            raise
        finally:
            session.close()

    def obtener_movimientos_inventario(
        self,
        producto_id: Optional[int] = None,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None,
    ) -> List[Inventario]:
        """
        Obtener movimientos de inventario
        
        Args:
            producto_id: Filtrar por producto
            fecha_inicio: Filtrar desde fecha
            fecha_fin: Filtrar hasta fecha
            
        Returns:
            Lista de movimientos
        """
        try:
            session = self.db.get_session()
            
            query = session.query(Inventario)
            
            if producto_id:
                query = query.filter_by(producto_id=producto_id)
            
            if fecha_inicio:
                query = query.filter(Inventario.fecha >= fecha_inicio)
            
            if fecha_fin:
                query = query.filter(Inventario.fecha <= fecha_fin)
            
            movimientos = query.order_by(Inventario.fecha.desc()).all()
            return movimientos
            
        except Exception as e:
            logger.error(f"Error obteniendo movimientos de inventario: {e}")
            raise
        finally:
            session.close()

    def obtener_producto(self, producto_id: int) -> Optional[Producto]:
        """
        Obtener datos de un producto
        
        Args:
            producto_id: ID del producto
            
        Returns:
            Producto o None
        """
        try:
            session = self.db.get_session()
            producto = session.query(Producto).filter_by(id=producto_id).first()
            return producto
        except Exception as e:
            logger.error(f"Error obteniendo producto: {e}")
            raise
        finally:
            session.close()
