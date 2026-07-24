"""Sistema de respaldo (backup) de base de datos"""

import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, List
from loguru import logger

from config.settings import settings


class SistemaRespaldo:
    """Clase para gestionar respaldos de base de datos"""

    def __init__(self):
        """Inicializar sistema de respaldo"""
        self.backup_dir = settings.backup_dir
        self.db_path = settings.get_db_path()
        logger.info(f"Sistema de respaldo inicializado. Directorio: {self.backup_dir}")

    def crear_respaldo(self, descripcion: Optional[str] = None) -> Optional[str]:
        """
        Crear respaldo de la base de datos
        
        Args:
            descripcion: Descripción del respaldo
            
        Returns:
            Ruta del archivo de respaldo creado o None si hay error
        """
        try:
            # Generar nombre del archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            desc_parte = f"_{descripcion}" if descripcion else ""
            nombre_archivo = f"backup_{timestamp}{desc_parte}.db"
            ruta_respaldo = self.backup_dir / nombre_archivo
            
            # Copiar archivo de BD
            shutil.copy2(self.db_path, str(ruta_respaldo))
            
            logger.info(f"Respaldo creado: {ruta_respaldo}")
            return str(ruta_respaldo)
            
        except Exception as e:
            logger.error(f"Error creando respaldo: {e}")
            return None

    def restaurar_respaldo(self, ruta_respaldo: str, crear_respaldo_actual: bool = True) -> bool:
        """
        Restaurar desde un respaldo
        
        Args:
            ruta_respaldo: Ruta del archivo de respaldo
            crear_respaldo_actual: Si True, crea un respaldo de la BD actual antes de restaurar
            
        Returns:
            True si se restauró exitosamente, False en caso contrario
        """
        try:
            ruta_respaldo = Path(ruta_respaldo)
            
            if not ruta_respaldo.exists():
                logger.error(f"Archivo de respaldo no existe: {ruta_respaldo}")
                return False
            
            # Crear respaldo de la BD actual si se solicita
            if crear_respaldo_actual:
                self.crear_respaldo("pre_restauracion")
            
            # Restaurar
            shutil.copy2(str(ruta_respaldo), self.db_path)
            
            logger.info(f"Base de datos restaurada desde: {ruta_respaldo}")
            return True
            
        except Exception as e:
            logger.error(f"Error restaurando respaldo: {e}")
            return False

    def listar_respaldos(self) -> List[dict]:
        """
        Listar todos los respaldos disponibles
        
        Returns:
            Lista de diccionarios con información de respaldos
        """
        try:
            respaldos = []
            
            for archivo in sorted(self.backup_dir.glob("backup_*.db")):
                stat = archivo.stat()
                respaldos.append({
                    "nombre": archivo.name,
                    "ruta": str(archivo),
                    "tamano": stat.st_size,
                    "fecha_creacion": datetime.fromtimestamp(stat.st_ctime),
                    "fecha_modificacion": datetime.fromtimestamp(stat.st_mtime),
                })
            
            return sorted(respaldos, key=lambda x: x["fecha_creacion"], reverse=True)
            
        except Exception as e:
            logger.error(f"Error listando respaldos: {e}")
            return []

    def eliminar_respaldo(self, ruta_respaldo: str) -> bool:
        """
        Eliminar un respaldo
        
        Args:
            ruta_respaldo: Ruta del archivo de respaldo
            
        Returns:
            True si se eliminó exitosamente
        """
        try:
            ruta = Path(ruta_respaldo)
            
            if not ruta.exists():
                logger.error(f"Archivo no existe: {ruta_respaldo}")
                return False
            
            ruta.unlink()
            logger.info(f"Respaldo eliminado: {ruta_respaldo}")
            return True
            
        except Exception as e:
            logger.error(f"Error eliminando respaldo: {e}")
            return False

    def eliminar_respaldos_antiguos(self, dias: int = 30) -> int:
        """
        Eliminar respaldos más antiguos que N días
        
        Args:
            dias: Días de antigüedad
            
        Returns:
            Número de respaldos eliminados
        """
        try:
            import time
            
            ahora = time.time()
            tiempo_limite = ahora - (dias * 24 * 3600)
            eliminados = 0
            
            for archivo in self.backup_dir.glob("backup_*.db"):
                if archivo.stat().st_mtime < tiempo_limite:
                    archivo.unlink()
                    eliminados += 1
                    logger.info(f"Respaldo antiguo eliminado: {archivo.name}")
            
            if eliminados > 0:
                logger.info(f"Se eliminaron {eliminados} respaldos antiguos")
            
            return eliminados
            
        except Exception as e:
            logger.error(f"Error eliminando respaldos antiguos: {e}")
            return 0
