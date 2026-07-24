"""Gestor de caja registradora"""

from datetime import datetime
from typing import List, Optional
from loguru import logger
from decimal import Decimal, ROUND_HALF_UP

from database.models import Caja
from database.connection import get_db
from config.constants import ESTADO_CAJA


class GestorCaja:
    """Clase para gestionar la caja registradora"""

    def __init__(self):
        """Inicializar gestor de caja"""
        self.db = get_db()
        logger.info("Gestor de caja inicializado")

    def abrir_caja(
        self,
        numero_caja: int,
        usuario_id: int,
        monto_inicial: float = 0,
    ) -> Caja:
        """
        Abrir caja registradora
        
        Args:
            numero_caja: Número de la caja
            usuario_id: ID del usuario que abre la caja
            monto_inicial: Monto de apertura (fondo inicial)
            
        Returns:
            Caja abierta
        """
        try:
            session = self.db.get_session()
            
            # Verificar que no haya caja abierta para este usuario
            caja_abierta = session.query(Caja).filter_by(
                usuario_id=usuario_id,
                estado=ESTADO_CAJA.ABIERTA,
            ).first()
            
            if caja_abierta:
                raise ValueError(
                    f"Usuario ya tiene caja abierta: {caja_abierta.id}"
                )
            
            caja = Caja(
                numero_caja=numero_caja,
                usuario_id=usuario_id,
                fecha_apertura=datetime.now(),
                estado=ESTADO_CAJA.ABIERTA,
                monto_inicial=monto_inicial,
            )
            
            session.add(caja)
            session.commit()
            
            logger.info(f"Caja {numero_caja} abierta por usuario {usuario_id}")
            return caja
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error abriendo caja: {e}")
            raise
        finally:
            session.close()

    def cerrar_caja(
        self,
        caja_id: int,
        monto_final: float,
        nota: Optional[str] = None,
    ) -> Caja:
        """
        Cerrar caja registradora
        
        Args:
            caja_id: ID de la caja
            monto_final: Monto final en caja
            nota: Notas adicionales
            
        Returns:
            Caja cerrada
        """
        try:
            session = self.db.get_session()
            
            caja = session.query(Caja).filter_by(id=caja_id).first()
            if not caja:
                raise ValueError(f"Caja {caja_id} no existe")
            
            if caja.estado != ESTADO_CAJA.ABIERTA:
                raise ValueError(f"Caja {caja_id} no está abierta")
            
            # Calcular diferencia
            diferencia = Decimal(str(monto_final)) - Decimal(str(caja.monto_inicial))
            
            # Actualizar caja
            caja.fecha_cierre = datetime.now()
            caja.monto_final = monto_final
            caja.diferencia = float(diferencia)
            caja.estado = ESTADO_CAJA.CERRADA
            caja.nota = nota
            
            session.commit()
            
            logger.info(
                f"Caja {caja_id} cerrada. Diferencia: {diferencia} "
                f"Inicial: {caja.monto_inicial} Final: {monto_final}"
            )
            return caja
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error cerrando caja: {e}")
            raise
        finally:
            session.close()

    def obtener_caja_abierta(self, usuario_id: int) -> Optional[Caja]:
        """
        Obtener caja abierta de un usuario
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            Caja abierta o None
        """
        try:
            session = self.db.get_session()
            
            caja = session.query(Caja).filter_by(
                usuario_id=usuario_id,
                estado=ESTADO_CAJA.ABIERTA,
            ).first()
            
            return caja
            
        except Exception as e:
            logger.error(f"Error obteniendo caja abierta: {e}")
            raise
        finally:
            session.close()

    def obtener_caja(self, caja_id: int) -> Optional[Caja]:
        """
        Obtener datos de una caja
        
        Args:
            caja_id: ID de la caja
            
        Returns:
            Caja o None
        """
        try:
            session = self.db.get_session()
            caja = session.query(Caja).filter_by(id=caja_id).first()
            return caja
        except Exception as e:
            logger.error(f"Error obteniendo caja: {e}")
            raise
        finally:
            session.close()

    def obtener_cajas_por_fecha(
        self,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        usuario_id: Optional[int] = None,
    ) -> List[Caja]:
        """
        Obtener cajas cerradas en un rango de fechas
        
        Args:
            fecha_inicio: Fecha de inicio
            fecha_fin: Fecha de fin
            usuario_id: Filtrar por usuario (opcional)
            
        Returns:
            Lista de cajas
        """
        try:
            session = self.db.get_session()
            
            query = session.query(Caja).filter(
                Caja.estado == ESTADO_CAJA.CERRADA,
                Caja.fecha_cierre >= fecha_inicio,
                Caja.fecha_cierre <= fecha_fin,
            )
            
            if usuario_id:
                query = query.filter_by(usuario_id=usuario_id)
            
            cajas = query.order_by(Caja.fecha_cierre.desc()).all()
            return cajas
            
        except Exception as e:
            logger.error(f"Error obteniendo cajas por fecha: {e}")
            raise
        finally:
            session.close()

    def calcular_resumen_caja(self, caja_id: int) -> dict:
        """
        Calcular resumen de una caja
        
        Args:
            caja_id: ID de la caja
            
        Returns:
            Dict con resumen de caja
        """
        try:
            session = self.db.get_session()
            
            caja = session.query(Caja).filter_by(id=caja_id).first()
            if not caja:
                raise ValueError(f"Caja {caja_id} no existe")
            
            # Obtener ventas asociadas a esta caja
            from database.models import Venta
            
            ventas = session.query(Venta).filter(
                Venta.fecha_venta >= caja.fecha_apertura,
                Venta.fecha_venta <= caja.fecha_cierre or datetime.now(),
            ).all()
            
            total_ventas = sum(v.total for v in ventas)
            cantidad_ventas = len(ventas)
            
            return {
                "caja_id": caja_id,
                "numero_caja": caja.numero_caja,
                "monto_inicial": caja.monto_inicial,
                "total_ventas": total_ventas,
                "cantidad_ventas": cantidad_ventas,
                "monto_final_esperado": caja.monto_inicial + total_ventas,
                "monto_final_real": caja.monto_final,
                "diferencia": caja.diferencia,
                "fecha_apertura": caja.fecha_apertura,
                "fecha_cierre": caja.fecha_cierre,
            }
            
        except Exception as e:
            logger.error(f"Error calculando resumen de caja: {e}")
            raise
        finally:
            session.close()
