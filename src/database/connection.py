"""Conexión a la base de datos"""

import os
from typing import Optional
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from loguru import logger
from config.settings import settings
from .models import Base


class Database:
    """Clase para gestionar la conexión a la base de datos"""

    def __init__(self, db_path: Optional[str] = None):
        """Inicializar conexión a BD"""
        self.db_path = db_path or settings.get_db_path()
        self.engine = None
        self.SessionLocal = None
        self._initialize()

    def _initialize(self) -> None:
        """Inicializar motor de BD y crear tablas"""
        try:
            # Crear URI de conexión
            db_uri = f"sqlite:///{self.db_path}"
            
            # Crear motor
            self.engine = create_engine(
                db_uri,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
                echo=False,
            )
            
            # Habilitar foreign keys en SQLite
            @event.listens_for(self.engine, "connect")
            def set_sqlite_pragma(dbapi_conn, connection_record):
                cursor = dbapi_conn.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
            
            # Crear todas las tablas
            Base.metadata.create_all(bind=self.engine)
            
            # Crear factory de sesiones
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
            )
            
            logger.info(f"Base de datos inicializada: {self.db_path}")
        except Exception as e:
            logger.error(f"Error inicializando base de datos: {e}")
            raise

    def get_session(self) -> Session:
        """Obtener nueva sesión de BD"""
        if self.SessionLocal is None:
            raise RuntimeError("Base de datos no inicializada")
        return self.SessionLocal()

    def close(self) -> None:
        """Cerrar conexión de BD"""
        if self.engine:
            self.engine.dispose()
            logger.info("Conexión de base de datos cerrada")

    def create_tables(self) -> None:
        """Crear todas las tablas"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Tablas creadas/verificadas")
        except Exception as e:
            logger.error(f"Error creando tablas: {e}")
            raise

    def drop_tables(self) -> None:
        """Eliminar todas las tablas (CUIDADO!)"""
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.warning("Todas las tablas han sido eliminadas")
        except Exception as e:
            logger.error(f"Error eliminando tablas: {e}")
            raise

    def vacuum(self) -> None:
        """Optimizar base de datos"""
        try:
            session = self.get_session()
            session.execute("VACUUM")
            session.close()
            logger.info("Base de datos optimizada")
        except Exception as e:
            logger.error(f"Error optimizando base de datos: {e}")


# Instancia global de base de datos
_db_instance: Optional[Database] = None


def init_db(db_path: Optional[str] = None) -> Database:
    """Inicializar base de datos global"""
    global _db_instance
    _db_instance = Database(db_path)
    return _db_instance


def get_db() -> Database:
    """Obtener instancia global de base de datos"""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance
