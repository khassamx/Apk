#!/data/data/com.termux/files/usr/bin/python3
import os
import sys
import subprocess

def run(cmd):
    """Ejecuta un comando y muestra salida en tiempo real"""
    process = subprocess.Popen(cmd, shell=True)
    process.communicate()

print("🔥 Bienvenido al Generador de APK desde GitHub 🔥")
repo_url = input("Introduce la URL del repositorio GitHub: ").strip()
app_name = input("Nombre para tu app (ej: MiApp): ").strip()

home = os.getenv("HOME")
project_path = f"{home}/{app_name}"

# 1️⃣ Clonar repo
if os.path.exists(project_path):
    print(f"❌ La carpeta {app_name} ya existe, borrando...")
    run(f"rm -rf {project_path}")

print(f"📂 Clonando {repo_url} en {project_path}...")
run(f"git clone {repo_url} {project_path}")

# 2️⃣ Crear proyecto Cordova
os.chdir(home)
if os.path.exists(f"{home}/{app_name}_cordova"):
    run(f"rm -rf {home}/{app_name}_cordova")
print(f"⚡ Creando proyecto Cordova {app_name}_cordova...")
run(f"cordova create {app_name}_cordova")
cordova_path = f"{home}/{app_name}_cordova"
os.chdir(cordova_path)

# 3️⃣ Añadir plataforma Android
print("📱 Añadiendo plataforma Android...")
run("cordova platform add android")

# 4️⃣ Copiar archivos del repo al www/
print("📁 Copiando archivos del repo a Cordova www/...")
run(f"cp -r {project_path}/* www/")

# 5️⃣ Construir APK
print("🛠️ Construyendo APK...")
run("cordova build android")

# 6️⃣ Mover APK a Descargas
apk_src = f"{cordova_path}/platforms/android/app/build/outputs/apk/debug/app-debug.apk"
apk_dest = f"{home}/storage/shared/Download/{app_name}.apk"

if os.path.exists(apk_src):
    run(f"cp {apk_src} {apk_dest}")
    print(f"✅ APK generada y guardada en: {apk_dest}")
else:
    print("❌ No se pudo generar la APK, revisa errores en la compilación.")