[app]

# Información de la aplicación
title = YeraPOV - POS
package.name = yerapov
package.domain = org.tresclaveles

# Archivo principal
source.dir = src
source.include_exts = py,png,jpg,kv,atlas,sqlite

# Versión
version = 1.0.0
requirements = python3,kivy,kivymd,sqlalchemy,pyjnius,plyer,requests,openpyxl,python-barcode,bcrypt,pyjwt,loguru,colorama

# Orientación y tamaño mínimo
orientations = portrait,landscape
fullscreen = 0
requirement.api = 31
requirement.arch = arm64-v8a

# Permisos Android
android.permissions = INTERNET,CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,ACCESS_FINE_LOCATION,VIBRATE,RECORD_AUDIO

# Características requeridas
android.features = android.hardware.camera,android.hardware.camera.autofocus,android.hardware.microphone

# Presencia de ubicación
p4a.url = https://github.com/kivy/python-for-android/releases/download/2023.12.0/python-for-android-2023.12.0.tar.gz
p4a.private_storage = True

# Información de compilación
android.gradle_dependencies = androidx.appcompat:appcompat:1.6.1

# Modo de compilación
p4a.bootstrap = webview
p4a.arch = arm64-v8a

# Alias de variables
android.release_artifact = aab

[buildozer]

# Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# Máximo de workers simultáneos
warn_on_root = 1
