# YeraPOV - Sistema de Punto de Venta e Inventario

Aplicación profesional **100% offline** de Punto de Venta (POS) e Inventario desarrollada en Python con PySide6 y SQLite.

## 🎯 Características

- ✅ **Operación 100% Offline** - No requiere conexión a internet
- ✅ **Gestión de Usuarios** - Control de acceso con roles (Admin, Vendedor, Gerente)
- ✅ **Gestión de Inventario** - Control de stock, categorías y códigos de barras
- ✅ **Punto de Venta** - Interfaz intuitiva para registro de ventas
- ✅ **Reportes** - Ventas, inventario, usuarios, cierre de caja
- ✅ **Respaldo Automático** - Backup de base de datos
- ✅ **Interfaz Moderna** - Diseño responsive en español
- ✅ **Escalable** - Arquitectura MVC modular y extensible

## 📋 Requisitos

- Python 3.9+
- Windows 10/11
- 100 MB de espacio en disco

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tresclavelessrl-cmyk/YeraPOV.git
cd YeraPOV
```

### 2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación
```bash
python main.py
```

## 📁 Estructura del Proyecto

```
YeraPOV/
├── main.py                      # Punto de entrada
├── config.py                    # Configuración global
├── requirements.txt             # Dependencias
├── README.md                    # Este archivo
│
├── src/
│   ├── database/               # Capa de datos
│   │   ├── __init__.py
│   │   ├── connection.py       # Conexión a SQLite
│   │   ├── migrations.py       # Inicialización de BD
│   │   └── queries.py          # Consultas SQL reutilizables
│   │
│   ├── models/                 # Modelos de datos
│   │   ├── __init__.py
│   │   ├── user.py            # Modelo de Usuario
│   │   ├── product.py         # Modelo de Producto
│   │   ├── sale.py            # Modelo de Venta
│   │   ├── inventory.py       # Modelo de Inventario
│   │   └── cash_register.py   # Modelo de Caja
│   │
│   ├── services/               # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── user_service.py    # Gestión de usuarios
│   │   ├── product_service.py # Gestión de productos
│   │   ├── sale_service.py    # Gestión de ventas
│   │   ├── inventory_service.py # Gestión de inventario
│   │   ├── cash_service.py    # Gestión de caja
│   │   └── auth_service.py    # Autenticación
│   │
│   ├── ui/                     # Interfaz gráfica (PySide6)
│   │   ├── __init__.py
│   │   ├── main_window.py     # Ventana principal
│   │   ├── login_window.py    # Ventana de login
│   │   ├── dialogs/           # Diálogos y ventanas emergentes
│   │   │   ├── __init__.py
│   │   │   ├── sale_dialog.py
│   │   │   ├── product_dialog.py
│   │   │   ├── user_dialog.py
│   │   │   └── cash_dialog.py
│   │   ├── widgets/           # Componentes reutilizables
│   │   │   ├── __init__.py
│   │   │   ├── sales_table.py
│   │   │   ├── inventory_table.py
│   │   │   └── utils_widgets.py
│   │   └── styles/            # Estilos CSS
│   │       ├── __init__.py
│   │       └── app_style.py
│   │
│   ├── reports/                # Generación de reportes
│   │   ├── __init__.py
│   │   ├── report_generator.py # Clase base
│   │   ├── sales_report.py    # Reporte de ventas
│   │   ├── inventory_report.py # Reporte de inventario
│   │   ├── user_report.py     # Reporte de usuarios
│   │   └── export/            # Exportación
│   │       ├── __init__.py
│   │       ├── pdf_export.py
│   │       └── excel_export.py
│   │
│   ├── utils/                  # Utilidades
│   │   ├── __init__.py
│   │   ├── validators.py      # Validaciones
│   │   ├── helpers.py         # Funciones auxiliares
│   │   ├── logger.py          # Sistema de logs
│   │   ├── exceptions.py      # Excepciones personalizadas
│   │   └── constants.py       # Constantes
│   │
│   ├── assets/                 # Recursos
│   │   ├── icons/             # Iconos de la aplicación
│   │   ├── images/            # Imágenes
│   │   └── data/              # Datos de demostración
│
├── tests/                       # Pruebas unitarias
│   ├── __init__.py
│   ├─��� test_models.py
│   ├── test_services.py
│   └── test_database.py
│
└── backups/                     # Respaldos automáticos
    └── .gitkeep
```

## 🏗️ Arquitectura MVC

La aplicación sigue el patrón **Model-View-Controller**:

- **Model** (src/models/): Representa la estructura de datos
- **View** (src/ui/): Interfaz gráfica con PySide6
- **Controller** (src/services/): Lógica de negocio
- **Data Access** (src/database/): Capa de persistencia

## 🔐 Credenciales de Demostración

Al ejecutar por primera vez, usa:
- **Usuario**: `admin`
- **Contraseña**: `1234`

## 📊 Funcionalidades Principales

### 1. Gestión de Usuarios
- Crear, editar y eliminar usuarios
- Asignar roles (Admin, Vendedor, Gerente)
- Control de acceso por funcionalidad
- Historial de actividad

### 2. Gestión de Inventario
- Registro de productos con códigos de barras
- Control de stock en tiempo real
- Categorización de productos
- Alertas de stock bajo

### 3. Punto de Venta
- Búsqueda rápida de productos
- Lectura de códigos de barras
- Cálculo automático de totales
- Descuentos y promociones
- Recibos en 58/80 mm
- Cierre de caja diario

### 4. Reportes y Exportación
- Reporte de ventas por período
- Reporte de inventario
- Reporte de usuarios
- Exportación a Excel y PDF

### 5. Respaldo y Seguridad
- Backup automático de base de datos
- Restauración de datos
- Encriptación de contraseñas
- Validaciones de entrada

## 🛠️ Configuración

Edita `config.py` para personalizar:
- Nombre de la empresa
- Ruta de la base de datos
- Formato de recibos
- Rutas de respaldo
- Idioma y moneda

## 📝 Uso Básico

### Iniciar Sesión
1. Ejecuta `python main.py`
2. Ingresa usuario y contraseña
3. Selecciona el rol si tienes múltiples

### Realizar una Venta
1. Ve a **Punto de Venta**
2. Escanea código de barras o busca producto
3. Ajusta cantidad
4. Confirma venta
5. Imprime o envía recibo

### Gestionar Inventario
1. Ve a **Inventario**
2. Agrega, edita o elimina productos
3. Actualiza stock manualmente o automáticamente
4. Genera reportes

## 🐛 Solución de Problemas

### Error: "No se puede conectar a la base de datos"
- Verifica que la carpeta `data/` existe
- Elimina `data/pos_system.db` y reinicia

### Error: "Módulo PySide6 no encontrado"
- Ejecuta: `pip install --upgrade PySide6`

### Acceso denegado en respaldo
- Verifica permisos en la carpeta `backups/`

## 🔄 Respaldo y Recuperación

### Respaldo Automático
Se realiza diariamente a las 23:55

### Respaldo Manual
```python
from src.utils.helpers import backup_database
backup_database()
```

### Restaurar Backup
```python
from src.utils.helpers import restore_database
restore_database('backups/2026-07-24_backup.db')
```

## 📈 Roadmap

- [ ] Sincronización en la nube
- [ ] App móvil para clientes
- [ ] Integración con pasarelas de pago
- [ ] IA para predicción de demanda
- [ ] Dashboard analítico avanzado
- [ ] Sistema de lealtad de clientes

## 🤝 Contribuir

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia Boost Software License 1.0 - ver archivo LICENSE para detalles.

## 📞 Soporte

Para reportar problemas o sugerencias:
- Abre un [Issue](https://github.com/tresclavelessrl-cmyk/YeraPOV/issues)
- Contacta: tresclavelessrl@ejemplo.com

---Quiero convertir este proyecto YeraPOV, actualmente desarrollado en Python + PySide6 + SQLite, en una aplicación Android nativa.

OBJETIVO PRINCIPAL:
Crear una aplicación Android llamada YeraNova POS, instalable mediante APK y compatible con Android 5.0 y superiores.

REQUISITO CRÍTICO:
La aplicación Android debe utilizar Kotlin + Jetpack Compose + Room/SQLite.
NO utilizar PySide6 en Android.
NO crear una aplicación web.
NO utilizar WebView como sustituto de una aplicación Android nativa.

COMPATIBILIDAD:
- minSdk = 21 (Android 5.0/API 21)
- targetSdk actualizado compatible con el proyecto
- Java/JDK 17
- Kotlin
- Jetpack Compose
- Room para base de datos local
- Funcionamiento 100% offline

UTILIZAR COMO REFERENCIA EL PROYECTO PYTHON EXISTENTE:

main.py
config.py
src/database/
src/models/
src/services/
src/ui/
src/reports/
src/utils/
tests/

ANALIZA TODO EL CÓDIGO PYTHON EXISTENTE ANTES DE CREAR LA VERSIÓN ANDROID.

MAPEO DE ARQUITECTURA:

Python:
src/models/
→ Kotlin data classes / Room entities

src/database/
→ Room Database + DAO

src/services/
→ Kotlin services/repositories

src/ui/
→ Jetpack Compose screens

src/reports/
→ generación/exportación de reportes compatible con Android

SQLite:
→ Room Database

PySide6:
→ reemplazar completamente por Jetpack Compose.

FUNCIONES QUE DEBE CONSERVAR:

1. Usuarios y autenticación.
2. Productos.
3. Inventario.
4. Ventas.
5. Caja.
6. Reportes.
7. Exportación.
8. Respaldos cuando sean apropiados.
9. Funcionamiento offline.

INTERFAZ PRINCIPAL DE INVENTARIO:

PRODUCTO | INICIO | ENTRADA | VENTA | FINAL | VENDIDO | PRECIO | IMPORTE

FÓRMULAS:

VENTA = INICIO + ENTRADA

VENDIDO = VENTA - FINAL

IMPORTE = VENDIDO × PRECIO

TOTAL = suma de todos los IMPORTES

El campo INICIO del siguiente día debe poder obtenerse automáticamente del FINAL del día anterior.

REQUISITOS DE DATOS:
- No eliminar datos existentes por defecto.
- No utilizar fallbackToDestructiveMigration() para producción.
- No insertar datos de demostración automáticamente.
- La base de datos debe funcionar localmente y sin conexión a Internet.
- Validar entradas numéricas y evitar cantidades negativas cuando no correspondan.
- Mantener integridad de las operaciones de inventario, ventas y caja.

ESTRUCTURA ANDROID DESEADA:

YeraPOV/
├── app/
│   ├── src/
│   │   └── main/
│   │       ├── java/.../
│   │       │   ├── data/
│   │       │   ├── database/
│   │       │   ├── models/
│   │       │   ├──

**Desarrollado por YeraNovaTechnologies S.R.L**
