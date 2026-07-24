"""Sistema de autenticación"""

from datetime import datetime, timedelta
from typing import Optional, Tuple
from loguru import logger
import jwt
import os

from database.models import Usuario
from .usuarios import GestorUsuarios
from config.settings import settings


class SistemaAutenticacion:
    """Sistema de autenticación y manejo de sesiones"""

    def __init__(self):
        """Inicializar sistema de autenticación"""
        self.gestor_usuarios = GestorUsuarios()
        self.secret_key = os.getenv("SECRET_KEY", "yerapov-secret-key-2024")
        self.timeout_sesion = settings.get("usuarios.sesion_timeout", 1800)  # 30 min
        logger.info("Sistema de autenticación inicializado")

    def autenticar(
        self, nombre_usuario: str, contrasena: str
    ) -> Tuple[bool, Optional[Usuario], Optional[str]]:
        """
        Autenticar usuario
        
        Args:
            nombre_usuario: Nombre de usuario
            contrasena: Contraseña
            
        Returns:
            Tupla (exitoso, usuario, token)
        """
        try:
            # Obtener usuario
            usuario = self.gestor_usuarios.obtener_usuario(
                nombre_usuario=nombre_usuario
            )
            
            if not usuario:
                logger.warning(f"Intento de login con usuario inexistente: {nombre_usuario}")
                return False, None, None
            
            if not usuario.activo:
                logger.warning(f"Intento de login con usuario inactivo: {nombre_usuario}")
                return False, None, None
            
            # Verificar contraseña
            if not GestorUsuarios.verificar_contrasena(
                contrasena, usuario.contrasena_hash
            ):
                logger.warning(f"Contraseña incorrecta para usuario: {nombre_usuario}")
                return False, None, None
            
            # Generar token
            token = self.generar_token(usuario)
            
            # Actualizar fecha de última conexión
            usuario.fecha_ultima_conexion = datetime.now()
            
            logger.info(f"Usuario autenticado: {nombre_usuario}")
            return True, usuario, token
            
        except Exception as e:
            logger.error(f"Error en autenticación: {e}")
            return False, None, None

    def generar_token(self, usuario: Usuario) -> str:
        """
        Generar JWT token para usuario
        
        Args:
            usuario: Objeto usuario
            
        Returns:
            Token JWT
        """
        try:
            payload = {
                "usuario_id": usuario.id,
                "nombre_usuario": usuario.nombre_usuario,
                "rol": usuario.rol.value,
                "exp": datetime.utcnow() + timedelta(seconds=self.timeout_sesion),
                "iat": datetime.utcnow(),
            }
            
            token = jwt.encode(payload, self.secret_key, algorithm="HS256")
            return token
            
        except Exception as e:
            logger.error(f"Error generando token: {e}")
            raise

    def verificar_token(self, token: str) -> Tuple[bool, Optional[dict]]:
        """
        Verificar y decodificar JWT token
        
        Args:
            token: Token JWT
            
        Returns:
            Tupla (válido, payload)
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return True, payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token expirado")
            return False, None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Token inválido: {e}")
            return False, None
        except Exception as e:
            logger.error(f"Error verificando token: {e}")
            return False, None

    def crear_usuario_default(self) -> Usuario:
        """
        Crear usuario administrador por defecto
        
        Returns:
            Usuario administrador creado
        """
        try:
            usuario = self.gestor_usuarios.crear_usuario(
                nombre_usuario="admin",
                nombre_completo="Administrador",
                contrasena="admin123",
                rol="administrador",
                correo="admin@yerapov.local",
            )
            logger.info("Usuario administrador por defecto creado")
            return usuario
        except ValueError as e:
            if "ya existe" in str(e):
                logger.info("Usuario administrador ya existe")
                return self.gestor_usuarios.obtener_usuario(nombre_usuario="admin")
            raise
