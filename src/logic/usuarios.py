"""Gestor de usuarios"""

from datetime import datetime
from typing import List, Optional
from loguru import logger
import bcrypt

from database.models import Usuario
from database.connection import get_db
from config.constants import ROLES


class GestorUsuarios:
    """Clase para gestionar usuarios"""

    def __init__(self):
        """Inicializar gestor de usuarios"""
        self.db = get_db()
        logger.info("Gestor de usuarios inicializado")

    @staticmethod
    def hashear_contrasena(contrasena: str) -> str:
        """
        Hashear contraseña con bcrypt
        
        Args:
            contrasena: Contraseña en texto plano
            
        Returns:
            Contraseña hasheada
        """
        salt = bcrypt.gensalt(rounds=10)
        return bcrypt.hashpw(contrasena.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def verificar_contrasena(contrasena: str, hash_contrasena: str) -> bool:
        """
        Verificar contraseña contra su hash
        
        Args:
            contrasena: Contraseña en texto plano
            hash_contrasena: Hash de la contraseña
            
        Returns:
            True si coinciden, False en caso contrario
        """
        return bcrypt.checkpw(
            contrasena.encode('utf-8'),
            hash_contrasena.encode('utf-8')
        )

    def crear_usuario(
        self,
        nombre_usuario: str,
        nombre_completo: str,
        contrasena: str,
        rol: str = "vendedor",
        correo: Optional[str] = None,
        telefono: Optional[str] = None,
    ) -> Usuario:
        """
        Crear nuevo usuario
        
        Args:
            nombre_usuario: Nombre de usuario
            nombre_completo: Nombre completo
            contrasena: Contraseña
            rol: Rol del usuario (administrador, gerente, vendedor, almacenero)
            correo: Correo electrónico
            telefono: Teléfono
            
        Returns:
            Usuario creado
        """
        try:
            session = self.db.get_session()
            
            # Validar que el usuario no exista
            existente = session.query(Usuario).filter_by(
                nombre_usuario=nombre_usuario
            ).first()
            if existente:
                raise ValueError(f"Usuario {nombre_usuario} ya existe")
            
            # Validar rol
            try:
                rol_enum = ROLES[rol.upper()]
            except KeyError:
                raise ValueError(f"Rol inválido: {rol}")
            
            # Hashear contraseña
            contrasena_hash = self.hashear_contrasena(contrasena)
            
            usuario = Usuario(
                nombre_usuario=nombre_usuario,
                nombre_completo=nombre_completo,
                contrasena_hash=contrasena_hash,
                rol=rol_enum,
                correo=correo,
                telefono=telefono,
                activo=True,
                fecha_creacion=datetime.now(),
            )
            
            session.add(usuario)
            session.commit()
            
            logger.info(f"Usuario creado: {nombre_usuario}")
            return usuario
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error creando usuario: {e}")
            raise
        finally:
            session.close()

    def obtener_usuario(
        self, usuario_id: Optional[int] = None, nombre_usuario: Optional[str] = None
    ) -> Optional[Usuario]:
        """
        Obtener usuario por ID o nombre de usuario
        
        Args:
            usuario_id: ID del usuario
            nombre_usuario: Nombre de usuario
            
        Returns:
            Usuario o None
        """
        try:
            session = self.db.get_session()
            
            if usuario_id:
                usuario = session.query(Usuario).filter_by(id=usuario_id).first()
            elif nombre_usuario:
                usuario = session.query(Usuario).filter_by(
                    nombre_usuario=nombre_usuario
                ).first()
            else:
                return None
            
            return usuario
            
        except Exception as e:
            logger.error(f"Error obteniendo usuario: {e}")
            raise
        finally:
            session.close()

    def listar_usuarios(self, activos_solo: bool = True) -> List[Usuario]:
        """
        Listar usuarios
        
        Args:
            activos_solo: Si es True, solo retorna usuarios activos
            
        Returns:
            Lista de usuarios
        """
        try:
            session = self.db.get_session()
            
            query = session.query(Usuario)
            
            if activos_solo:
                query = query.filter_by(activo=True)
            
            usuarios = query.order_by(Usuario.nombre_completo).all()
            return usuarios
            
        except Exception as e:
            logger.error(f"Error listando usuarios: {e}")
            raise
        finally:
            session.close()

    def actualizar_usuario(
        self,
        usuario_id: int,
        nombre_completo: Optional[str] = None,
        correo: Optional[str] = None,
        telefono: Optional[str] = None,
        rol: Optional[str] = None,
    ) -> Usuario:
        """
        Actualizar datos de usuario
        
        Args:
            usuario_id: ID del usuario
            nombre_completo: Nuevo nombre completo
            correo: Nuevo correo
            telefono: Nuevo teléfono
            rol: Nuevo rol
            
        Returns:
            Usuario actualizado
        """
        try:
            session = self.db.get_session()
            
            usuario = session.query(Usuario).filter_by(id=usuario_id).first()
            if not usuario:
                raise ValueError(f"Usuario {usuario_id} no existe")
            
            if nombre_completo:
                usuario.nombre_completo = nombre_completo
            
            if correo:
                usuario.correo = correo
            
            if telefono:
                usuario.telefono = telefono
            
            if rol:
                try:
                    usuario.rol = ROLES[rol.upper()]
                except KeyError:
                    raise ValueError(f"Rol inválido: {rol}")
            
            session.commit()
            logger.info(f"Usuario {usuario_id} actualizado")
            return usuario
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error actualizando usuario: {e}")
            raise
        finally:
            session.close()

    def cambiar_contrasena(self, usuario_id: int, nueva_contrasena: str) -> bool:
        """
        Cambiar contraseña de usuario
        
        Args:
            usuario_id: ID del usuario
            nueva_contrasena: Nueva contraseña
            
        Returns:
            True si se cambió exitosamente
        """
        try:
            session = self.db.get_session()
            
            usuario = session.query(Usuario).filter_by(id=usuario_id).first()
            if not usuario:
                raise ValueError(f"Usuario {usuario_id} no existe")
            
            usuario.contrasena_hash = self.hashear_contrasena(nueva_contrasena)
            session.commit()
            
            logger.info(f"Contraseña del usuario {usuario_id} cambiada")
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error cambiando contraseña: {e}")
            raise
        finally:
            session.close()

    def desactivar_usuario(self, usuario_id: int) -> bool:
        """
        Desactivar usuario
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            True si se desactivó exitosamente
        """
        try:
            session = self.db.get_session()
            
            usuario = session.query(Usuario).filter_by(id=usuario_id).first()
            if not usuario:
                raise ValueError(f"Usuario {usuario_id} no existe")
            
            usuario.activo = False
            session.commit()
            
            logger.info(f"Usuario {usuario_id} desactivado")
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error desactivando usuario: {e}")
            raise
        finally:
            session.close()
