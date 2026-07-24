# Sistema POS e Inventario Multiplataforma

**YeraPOV** - Sistema POS e Inventario offline para Windows y Android

## 🎯 Características

### 📱 Multiplataforma
- ✅ **Windows** - Aplicación PySide6 nativa
- ✅ **Android** - Usando Kivy/BeeWare/Buildozer
- ✅ SQLite sincronizado en ambas plataformas

### 💼 Gestión de Ventas
- **Fórmula Automática**: Inicio + Entrada = Venta
- **Cálculo Automático**: Venta - Final = Vendido
- **Importe**: Vendido × Precio = Total automático
- Interfaz tipo Excel para entrada rápida de datos

### 🏪 Características Principales
- 👤 Gestión de usuarios con roles y permisos
- 💰 Control de caja (apertura/cierre)
- 📊 Códigos de barras (lectura y generación)
- 🧾 Tickets 58mm y 80mm
- 📁 Importación/Exportación Excel
- 📄 Generación de reportes PDF
- 💾 Sistema de respaldo automático
- 🌙 Tema claro/oscuro
- 🇪🇸 Interfaz completamente en español

## 📁 Estructura del Proyecto

```
YeraPOV/
├── src/
│   ├── main.py                 # Punto de entrada Windows
│   ├── main_android.py         # Punto de entrada Android
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py         # Configuración de la aplicación
│   │   └── constants.py        # Constantes globales
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py           # Modelos SQLAlchemy/ORM
│   │   ├── connection.py       # Conexión a BD
│   │   └── migrations.py       # Migraciones
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── windows/            # Pantallas PySide6 (Windows)
│   │   │   ├── __init__.py
│   │   │   ├── main_window.py
│   │   │   ├── login.py
│   │   │   ├── ventas.py
│   │   │   ├── inventario.py
│   │   │   ├── usuarios.py
│   │   │   ├── caja.py
│   │   │   └── reportes.py
│   │   ├── screens/            # Pantallas Kivy (Android)
│   │   │   ├── __init__.py
│   │   │   ├── login_screen.py
│   │   │   ├── venta_screen.py
│   │   │   ├── inventario_screen.py
│   │   │   └── reportes_screen.py
│   │   ├── styles/
│   │   │   ├── __init__.py
│   │   │   ├── styles.qss       # Estilos PySide6
│   │   │   └── theme.py         # Temas
│   │   └── resources/
│   │       ├── icons/
│   │       └── assets/
│   ├── logic/
│   │   ├── __init__.py
│   │   ├── ventas.py           # Lógica de ventas
│   │   ├── inventario.py       # Gestión inventario
│   │   ├── usuarios.py         # Gestión usuarios
│   │   ├── caja.py             # Control caja
│   │   ├── calculos.py         # Cálculos automáticos
│   │   └── autenticacion.py    # Sistema de autenticación
│   ├── reports/
│   │   ├── __init__.py
│   │   ├── tickets.py          # Generación tickets (58/80mm)
│   │   ├── pdf_generator.py    # Reportes PDF
│   │   ├── excel_export.py     # Exportación Excel
│   │   └── templates/          # Plantillas de reportes
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── barcode.py          # Generación códigos de barras
│   │   ├── scanner.py          # Lectura códigos de barras
│   │   ├── backup.py           # Sistema de respaldo
│   │   ├── validators.py       # Validadores
│   │   └── helpers.py          # Funciones auxiliares
│   └── api/
│       ├── __init__.py
│       └── sync.py             # Sincronización Windows/Android
├── tests/
│   ├── __init__.py
│   ├── test_ventas.py
│   ├── test_inventario.py
│   ├── test_calculos.py
│   └── test_usuarios.py
├── requirements.txt            # Dependencias Python
├── requirements_android.txt    # Dependencias Android (Kivy)
├── buildozer.spec              # Configuración Buildozer (Android)
├── setup.py                    # Setup para instalación
└── README.md                   # Este archivo
```

## 🚀 Instalación

### Windows

```bash
# Clonar repositorio
git clone https://github.com/tresclavelessrl-cmyk/YeraPOV.git
cd YeraPOV

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python src/main.py
```

### Android

```bash
# Instalar Buildozer y dependencias
pip install buildozer cython kivy

# Compilar APK
buildozer android debug

# O instalar directamente en dispositivo
buildozer android debug deploy run
```

## 📦 Dependencias Principales

### Windows (PySide6)
- `PySide6` - UI nativa
- `SQLAlchemy` - ORM
- `sqlite3` - Base de datos
- `openpyxl` - Excel
- `reportlab` - PDF
- `pyzbar` - Lectura códigos de barras
- `Pillow` - Procesamiento imágenes
- `python-barcode` - Generación códigos de barras
- `requests` - Sincronización

### Android (Kivy)
- `Kivy` - Framework UI multiplataforma
- `pyjnius` - Acceso APIs Android
- `plyer` - APIs nativas Android
- `SQLAlchemy` - ORM
- `sqlite3` - Base de datos
- `android-permissions` - Permisos

## 🎮 Funcionalidades Clave

### 1. Sistema de Ventas
```
┌─────────────────────────────────────┐
│ Inicio (Stock Inicial)    [1000]    │
│ + Entrada (Compra)        [+500]    │
│ = Venta (Disponible)      [1500]    │
│ - Final (Stock Actual)    [-300]    │
│ = Vendido (Salida)        [1200]    │
│ × Precio                  [×$10]    │
│ = IMPORTE TOTAL           [$12000]  │
└─────────────────────────────────────┘
```

### 2. Gestión de Usuarios
- Administrador
- Vendedor
- Gerente
- Almacenero
- Permisos customizables

### 3. Caja Registradora
- Apertura/Cierre de caja
- Arqueo de caja
- Registros de movimientos

### 4. Códigos de Barras
- Lectura en tiempo real
- Generación automática
- Múltiples formatos (EAN13, CODE128, etc)

### 5. Reportes
- Tickets 58mm (recibos)
- Tickets 80mm (etiquetas)
- PDF: Ventas, Inventario, Caja
- Excel: Exportación completa

### 6. Respaldo
- Backup automático
- Sincronización Windows ↔ Android
- Exportación/Importación

## 🔐 Seguridad

- Contraseñas hasheadas (bcrypt)
- Sesiones de usuario
- Registro de auditoría
- Permisos por rol
- Encriptación de datos sensibles

## 🌐 Sincronización Multiplataforma

```
Windows PC
    ↓
  [API REST]
    ↓
Android Device

- SQLite sync automático
- Cambios incrementales
- Conflicto resolution
```

## 📋 Estados del Proyecto

- [ ] Estructura base
- [ ] Modelos de BD
- [ ] UI Windows (PySide6)
- [ ] Lógica de ventas
- [ ] Sistema de caja
- [ ] Generación de reportes
- [ ] UI Android (Kivy)
- [ ] Sincronización
- [ ] Pruebas
- [ ] Documentación
- [ ] Build Android (APK)

## 👨‍💻 Desarrollo

```bash
# Crear rama feature
git checkout -b feature/nombre-feature

# Hacer cambios
# ...

# Commit
git add .
git commit -m "feat: descripción del cambio"

# Push
git push origin feature/nombre-feature

# Pull Request en GitHub
```

## 📝 Licencia

Boost Software License 1.0

## 👥 Autor

Tres Claveles S.R.L.

---

**Versión**: 1.0.0
**Última actualización**: 2026-07-24
