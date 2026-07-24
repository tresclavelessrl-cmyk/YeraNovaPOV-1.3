"""Validadores de datos"""

import re
from typing import Tuple
from loguru import logger

from config.constants import PATTERNS, LIMITS


class Validadores:
    """Clase con validadores de datos"""

    @staticmethod
    def validar_email(email: str) -> Tuple[bool, str]:
        """
        Validar formato de email
        
        Args:
            email: Email a validar
            
        Returns:
            Tupla (válido, mensaje)
        """
        if not email:
            return True, ""  # Email es opcional
        
        if len(email) > 100:
            return False, "Email muy largo (máximo 100 caracteres)"
        
        if not re.match(PATTERNS["email"], email):
            return False, "Formato de email inválido"
        
        return True, ""

    @staticmethod
    def validar_telefono(telefono: str) -> Tuple[bool, str]:
        """
        Validar formato de teléfono
        
        Args:
            telefono: Teléfono a validar
            
        Returns:
            Tupla (válido, mensaje)
        """
        if not telefono:
            return True, ""  # Teléfono es opcional
        
        if not re.match(PATTERNS["telefono"], telefono):
            return False, "Formato de teléfono inválido"
        
        return True, ""

    @staticmethod
    def validar_codigo_barras(codigo: str) -> Tuple[bool, str]:
        """
        Validar código de barras
        
        Args:
            codigo: Código de barras
            
        Returns:
            Tupla (válido, mensaje)
        """
        if not codigo:
            return False, "Código de barras no puede estar vacío"
        
        if not re.match(PATTERNS["codigo_barras"], codigo):
            return False, "Código de barras debe contener solo números (8-15 dígitos)"
        
        return True, ""

    @staticmethod
    def validar_contrasena(contrasena: str) -> Tuple[bool, str]:
        """
        Validar fortaleza de contraseña
        
        Args:
            contrasena: Contraseña a validar
            
        Returns:
            Tupla (válido, mensaje)
        """
        min_length = LIMITS["contrasena_minima"]
        
        if len(contrasena) < min_length:
            return False, f"Contraseña debe tener al menos {min_length} caracteres"
        
        # Validar complejidad
        tiene_mayuscula = any(c.isupper() for c in contrasena)
        tiene_minuscula = any(c.islower() for c in contrasena)
        tiene_numero = any(c.isdigit() for c in contrasena)
        tiene_especial = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in contrasena)
        
        complejidad = sum([tiene_mayuscula, tiene_minuscula, tiene_numero, tiene_especial])
        
        if complejidad < 3:
            return False, "Contraseña debe contener letras mayúsculas, minúsculas, números y caracteres especiales"
        
        return True, ""

    @staticmethod
    def validar_cantidad(cantidad: str) -> Tuple[bool, str, int]:
        """
        Validar cantidad numérica
        
        Args:
            cantidad: Cantidad a validar
            
        Returns:
            Tupla (válido, mensaje, valor_convertido)
        """
        try:
            valor = int(cantidad)
            
            if valor <= 0:
                return False, "Cantidad debe ser mayor a 0", 0
            
            return True, "", valor
            
        except ValueError:
            return False, "Cantidad debe ser un número entero válido", 0

    @staticmethod
    def validar_precio(precio: str) -> Tuple[bool, str, float]:
        """
        Validar precio numérico
        
        Args:
            precio: Precio a validar
            
        Returns:
            Tupla (válido, mensaje, valor_convertido)
        """
        try:
            valor = float(precio)
            
            if valor <= 0:
                return False, "Precio debe ser mayor a 0", 0
            
            return True, "", valor
            
        except ValueError:
            return False, "Precio debe ser un número válido", 0

    @staticmethod
    def validar_nombre_usuario(nombre_usuario: str) -> Tuple[bool, str]:
        """
        Validar nombre de usuario
        
        Args:
            nombre_usuario: Nombre de usuario
            
        Returns:
            Tupla (válido, mensaje)
        """
        max_length = LIMITS["nombre_usuario"]
        
        if not nombre_usuario:
            return False, "Nombre de usuario no puede estar vacío"
        
        if len(nombre_usuario) > max_length:
            return False, f"Nombre de usuario muy largo (máximo {max_length})"
        
        # Solo letras, números y guiones bajos
        if not re.match(r"^[a-zA-Z0-9_]+$", nombre_usuario):
            return False, "Nombre de usuario solo puede contener letras, números y guiones bajos"
        
        return True, ""
