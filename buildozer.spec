"""buildozer.spec

Buildozer permite crear APK/AAB para Android desde el código Kivy

Uso:
    buildozer android debug     # Crear APK debug
    buildozer android release   # Crear APK release
    buildozer android deploy    # Deploy a dispositivo

Requiere:
    - Java Development Kit (JDK)
    - Android SDK
    - Android NDK
"""

[app]

# (str) Título de la aplicación
title = YeraPOV POS

# (str) Nombre del paquete
package.name = yerapov

# (str) Dominio del paquete (en formato invertido)
package.domain = org.yerapov

# (source.dir) Directorio fuente
source.dir = .

# (source.include_exts) Extensiones a incluir
source.include_exts = py,png,jpg,kv,atlas

# (source.include_patterns) Patrones a incluir
source.include_patterns = data/*,assets/*

# (source.exclude_dirs) Directorios a excluir
source.exclude_dirs = tests,bin,venv

# (source.exclude_patterns) Patrones a excluir
source.exclude_patterns = *.pyc,*.pyo,__pycache__

# (version) Versión de la aplicación
version = 1.0.0

# (requirements) Dependencias de Python
requirements = python3,kivy,sqlalchemy,loguru,bcrypt,pyjwt

# (orientation) Orientación de la pantalla
orientation = portrait

# (icon.filename) Ícono de la aplicación
icon.filename = %(source.dir)s/assets/icon.png

# (presplash.filename) Pantalla de inicio
presplash.filename = %(source.dir)s/assets/presplash.png

# (presplash.scale) Escala de la pantalla de inicio
presplash.scale = 2

# (fullscreen) Modo pantalla completa
fullscreen = 0

# (android.permissions) Permisos de Android
android.permissions = INTERNET,CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (android.api) API de Android
android.api = 34

# (android.minapi) API mínimo de Android
android.minapi = 24

# (android.ndk) Versión del NDK
android.ndk = 26b

# (android.accept_sdk_license) Aceptar licencias del SDK
android.accept_sdk_license = True

[buildozer]

# (log_level) Nivel de logging
log_level = 2

# (warn_on_root) Advertencia al ejecutar como root
warn_on_root = 1
