"""Módulo para generación y lectura de códigos de barras"""

from typing import Optional, Tuple
from pathlib import Path
from loguru import logger
import barcode
from barcode.writer import ImageWriter
from PIL import Image
import io

try:
    from pyzbar.pyzbar import decode
    PYZBAR_DISPONIBLE = True
except ImportError:
    PYZBAR_DISPONIBLE = False
    logger.warning("pyzbar no disponible. Lectura de códigos de barras deshabilitada.")


class GeneradorCodigosBarras:
    """Clase para generar códigos de barras"""

    FORMATOS_SOPORTADOS = {
        "EAN13": barcode.ean13.EAN13,
        "EAN8": barcode.ean8.EAN8,
        "CODE128": barcode.code128.Code128,
        "CODE39": barcode.code39.Code39,
        "UPCA": barcode.upca.UPCA,
    }

    @staticmethod
    def generar_ean13(numero: str, ruta_salida: Optional[str] = None) -> Optional[str]:
        """
        Generar código de barras EAN13
        
        Args:
            numero: Número para el código de barras
            ruta_salida: Ruta donde guardar la imagen (sin extensión)
            
        Returns:
            Ruta del archivo generado o None si hay error
        """
        try:
            # Validar que sea un número válido para EAN13
            if not numero.isdigit() or len(numero) > 13:
                logger.error(f"Número inválido para EAN13: {numero}")
                return None
            
            # Rellenar con ceros a la izquierda si es necesario
            numero = numero.zfill(13)
            
            # Crear código de barras
            ean = barcode.ean13.EAN13(numero)
            
            if ruta_salida:
                ruta = ean.save(ruta_salida)
                logger.info(f"Código de barras EAN13 generado: {ruta}")
                return ruta
            else:
                # Retornar como imagen en memoria
                buffer = io.BytesIO()
                ean.write(buffer, format="png")
                return buffer
            
        except Exception as e:
            logger.error(f"Error generando EAN13: {e}")
            return None

    @staticmethod
    def generar_codigo128(numero: str, ruta_salida: Optional[str] = None) -> Optional[str]:
        """
        Generar código de barras CODE128
        
        Args:
            numero: Texto para el código de barras
            ruta_salida: Ruta donde guardar la imagen (sin extensión)
            
        Returns:
            Ruta del archivo generado o None si hay error
        """
        try:
            # Crear código de barras
            code = barcode.code128.Code128(numero)
            
            if ruta_salida:
                ruta = code.save(ruta_salida)
                logger.info(f"Código de barras CODE128 generado: {ruta}")
                return ruta
            else:
                # Retornar como imagen en memoria
                buffer = io.BytesIO()
                code.write(buffer, format="png")
                return buffer
            
        except Exception as e:
            logger.error(f"Error generando CODE128: {e}")
            return None

    @staticmethod
    def generar_barcode(
        numero: str,
        formato: str = "EAN13",
        ruta_salida: Optional[str] = None,
    ) -> Optional[str]:
        """
        Generar código de barras en formato especificado
        
        Args:
            numero: Número/texto para el código
            formato: Formato del código (EAN13, EAN8, CODE128, CODE39, UPCA)
            ruta_salida: Ruta donde guardar
            
        Returns:
            Ruta del archivo o None si hay error
        """
        try:
            if formato not in GeneradorCodigosBarras.FORMATOS_SOPORTADOS:
                logger.error(f"Formato no soportado: {formato}")
                return None
            
            codigo_clase = GeneradorCodigosBarras.FORMATOS_SOPORTADOS[formato]
            codigo = codigo_clase(numero)
            
            if ruta_salida:
                ruta = codigo.save(ruta_salida)
                logger.info(f"Código de barras {formato} generado: {ruta}")
                return ruta
            else:
                buffer = io.BytesIO()
                codigo.write(buffer, format="png")
                return buffer
            
        except Exception as e:
            logger.error(f"Error generando código de barras {formato}: {e}")
            return None


class LectorCodigosBarras:
    """Clase para leer códigos de barras"""

    @staticmethod
    def leer_imagen(ruta_imagen: str) -> Optional[str]:
        """
        Leer código de barras desde una imagen
        
        Args:
            ruta_imagen: Ruta a la imagen
            
        Returns:
            Código de barras leído o None
        """
        if not PYZBAR_DISPONIBLE:
            logger.error("pyzbar no disponible. No se puede leer códigos de barras.")
            return None
        
        try:
            imagen = Image.open(ruta_imagen)
            codigos = decode(imagen)
            
            if codigos:
                codigo = codigos[0].data.decode('utf-8')
                logger.info(f"Código de barras leído: {codigo}")
                return codigo
            else:
                logger.warning(f"No se encontró código de barras en: {ruta_imagen}")
                return None
            
        except Exception as e:
            logger.error(f"Error leyendo código de barras: {e}")
            return None

    @staticmethod
    def leer_camara(device_index: int = 0) -> Optional[str]:
        """
        Leer código de barras desde cámara
        
        Args:
            device_index: Índice del dispositivo de cámara
            
        Returns:
            Código de barras leído o None
        """
        if not PYZBAR_DISPONIBLE:
            logger.error("pyzbar no disponible. No se puede leer códigos de barras.")
            return None
        
        try:
            import cv2
        except ImportError:
            logger.error("OpenCV no disponible. No se puede usar cámara.")
            return None
        
        try:
            cap = cv2.VideoCapture(device_index)
            
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                codigos = decode(frame)
                
                if codigos:
                    codigo = codigos[0].data.decode('utf-8')
                    cap.release()
                    logger.info(f"Código de barras leído de cámara: {codigo}")
                    return codigo
                
                # Mostrar frame
                cv2.imshow('Lector Códigos de Barras', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            return None
            
        except Exception as e:
            logger.error(f"Error leyendo de cámara: {e}")
            return None
