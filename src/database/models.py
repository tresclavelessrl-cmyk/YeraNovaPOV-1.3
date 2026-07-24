"""Modelos de la base de datos"""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    Enum,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config.constants import (
    ROLES,
    ESTADO_VENTA,
    ESTADO_CAJA,
    BARCODE_FORMATS,
)

Base = declarative_base()


class Usuario(Base):
    """Modelo de usuario"""

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False, index=True)
    nombre_completo = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True)
    contrasena_hash = Column(String(255), nullable=False)
    rol = Column(Enum(ROLES), nullable=False, default=ROLES.VENDEDOR)
    activo = Column(Boolean, nullable=False, default=True)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.now)
    fecha_ultima_conexion = Column(DateTime)
    telefono = Column(String(20))
    
    # Relaciones
    ventas = relationship("Venta", back_populates="vendedor")
    movimientos_caja = relationship("Caja", back_populates="usuario")
    auditoria = relationship("AuditLog", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario {self.nombre_usuario}>"


class Producto(Base):
    """Modelo de producto"""

    __tablename__ = "productos"

    id = Column(Integer, primary_key=True)
    codigo_interno = Column(String(20), unique=True, nullable=False, index=True)
    codigo_barras = Column(String(50), unique=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    categoria = Column(String(50), nullable=False)
    precio_venta = Column(Float, nullable=False)
    precio_costo = Column(Float)
    stock_inicial = Column(Integer, nullable=False, default=0)
    stock_actual = Column(Integer, nullable=False, default=0)
    stock_minimo = Column(Integer, default=5)
    formato_barcode = Column(Enum(BARCODE_FORMATS), default=BARCODE_FORMATS.EAN13)
    activo = Column(Boolean, nullable=False, default=True)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.now)
    fecha_actualizacion = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    detalles_venta = relationship("DetalleVenta", back_populates="producto")
    movimientos_inventario = relationship("Inventario", back_populates="producto")

    def __repr__(self):
        return f"<Producto {self.nombre}>"


class Venta(Base):
    """Modelo de venta"""

    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True)
    numero_venta = Column(String(20), unique=True, nullable=False, index=True)
    fecha_venta = Column(DateTime, nullable=False, default=datetime.now, index=True)
    vendedor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cliente_nombre = Column(String(100))
    cliente_telefono = Column(String(20))
    cliente_email = Column(String(100))
    estado = Column(Enum(ESTADO_VENTA), nullable=False, default=ESTADO_VENTA.COMPLETADA)
    subtotal = Column(Float, nullable=False, default=0)
    descuento = Column(Float, default=0)
    impuesto = Column(Float, default=0)
    total = Column(Float, nullable=False, default=0)
    metodo_pago = Column(String(50))  # efectivo, tarjeta, transferencia, etc
    nota = Column(Text)
    
    # Relaciones
    vendedor = relationship("Usuario", back_populates="ventas")
    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Venta {self.numero_venta}>"


class DetalleVenta(Base):
    """Modelo de detalle de venta (items)"""

    __tablename__ = "detalles_venta"

    id = Column(Integer, primary_key=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    descuento_linea = Column(Float, default=0)
    subtotal = Column(Float, nullable=False)
    
    # Relaciones
    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_venta")

    def __repr__(self):
        return f"<DetalleVenta venta={self.venta_id} producto={self.producto_id}>"


class Caja(Base):
    """Modelo de caja registradora"""

    __tablename__ = "caja"

    id = Column(Integer, primary_key=True)
    numero_caja = Column(Integer, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_apertura = Column(DateTime, nullable=False, default=datetime.now, index=True)
    fecha_cierre = Column(DateTime)
    estado = Column(Enum(ESTADO_CAJA), nullable=False, default=ESTADO_CAJA.ABIERTA)
    monto_inicial = Column(Float, nullable=False, default=0)
    monto_final = Column(Float)
    diferencia = Column(Float)  # monto_final - monto_inicial
    nota = Column(Text)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="movimientos_caja")

    def __repr__(self):
        return f"<Caja {self.numero_caja} - {self.estado.value}>"


class Inventario(Base):
    """Modelo de movimiento de inventario"""

    __tablename__ = "inventario"

    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    tipo_movimiento = Column(String(20), nullable=False)  # entrada, salida, ajuste, devolucion
    cantidad = Column(Integer, nullable=False)
    stock_anterior = Column(Integer, nullable=False)
    stock_nuevo = Column(Integer, nullable=False)
    razon = Column(String(100))
    referencia = Column(String(50))  # número de venta, número de compra, etc
    fecha = Column(DateTime, nullable=False, default=datetime.now, index=True)
    
    # Relaciones
    producto = relationship("Producto", back_populates="movimientos_inventario")

    def __repr__(self):
        return f"<Inventario producto={self.producto_id} tipo={self.tipo_movimiento}>"


class AuditLog(Base):
    """Modelo de registro de auditoría"""

    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    accion = Column(String(100), nullable=False)
    tabla = Column(String(50), nullable=False)
    id_registro = Column(Integer)
    valores_anteriores = Column(Text)  # JSON
    valores_nuevos = Column(Text)  # JSON
    fecha = Column(DateTime, nullable=False, default=datetime.now, index=True)
    direccion_ip = Column(String(45))
    user_agent = Column(String(500))
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="auditoria")

    def __repr__(self):
        return f"<AuditLog {self.accion} en {self.tabla}>"
