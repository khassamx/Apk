import os
import shutil
import subprocess

# Configuración
APP_NAME = "MallyWearApp"
PACKAGE_NAME = "com.mallywear.app"
OUTPUT_DIR = os.path.expanduser("~/storage/shared/Download")
PROJECT_DIR = os.path.abspath("android_build")

# Limpieza de proyecto anterior
if os.path.exists(PROJECT_DIR):
    shutil.rmtree(PROJECT_DIR)

os.makedirs(PROJECT_DIR)

# Crear estructura mínima
os.makedirs(os.path.join(PROJECT_DIR, "app/src/main/assets"), exist_ok=True)
os.makedirs(os.path.join(PROJECT_DIR, "app/src/main/java", *PACKAGE_NAME.split(".")), exist_ok=True)
os.makedirs(os.path.join(PROJECT_DIR, "app/src/main/res/layout"), exist_ok=True)
os.makedirs(os.path.join(PROJECT_DIR, "app/src/main/res/values"), exist_ok=True)

# Copiar archivos web
for file in ["index.html", "style.css", "script.js"]:
    if os.path.exists(file):
        shutil.copy(file, os.path.join(PROJECT_DIR, "app/src/main/assets"))
    else:
        print(f"⚠️  {file} no encontrado, saltando...")

# Crear MainActivity.java
main_activity_path = os.path.join(PROJECT_DIR, "app/src/main/java", *PACKAGE_NAME.split("."), "MainActivity.java")
with open(main_activity_path, "w") as f:
    f.write(f"""
package {PACKAGE_NAME};

import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        WebView webView = new WebView(this);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.setWebViewClient(new WebViewClient());
        webView.loadUrl("file:///android_asset/index.html");
        setContentView(webView);
    }}
}}
""")

# Crear AndroidManifest.xml
manifest_path = os.path.join(PROJECT_DIR, "app/src/main/AndroidManifest.xml")
with open(manifest_path, "w") as f:
    f.write(f"""
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{PACKAGE_NAME}">
    <application android:allowBackup="true"
        android:label="{APP_NAME}"
        android:icon="@mipmap/ic_launcher"
        android:roundIcon="@mipmap/ic_launcher_round">
        <activity android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>
""")

# Crear build.gradle (app)
gradle_app_path = os.path.join(PROJECT_DIR, "app/build.gradle")
os.makedirs(os.path.dirname(gradle_app_path), exist_ok=True)
with open(gradle_app_path, "w") as f:
    f.write(f"""
plugins {{
    id 'com.android.application'
}}

android {{
    compileSdk 33

    defaultConfig {{
        applicationId "{PACKAGE_NAME}"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"
    }}

    buildTypes {{
        release {{
            minifyEnabled false
        }}
    }}
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.6.1'
}}
""")

# Crear build.gradle (root)
gradle_root_path = os.path.join(PROJECT_DIR, "build.gradle")
with open(gradle_root_path, "w") as f:
    f.write("""
buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:7.4.1'
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
""")

# Crear settings.gradle
with open(os.path.join(PROJECT_DIR, "settings.gradle"), "w") as f:
    f.write("include ':app'\n")

# Crear gradlew simple (llamará a gradle local)
with open(os.path.join(PROJECT_DIR, "gradlew"), "w") as f:
    f.write("""#!/bin/sh
gradle "$@"
""")
os.chmod(os.path.join(PROJECT_DIR, "gradlew"), 0o755)

# Iniciar compilación
print("🚀 Construyendo APK... Esto puede tardar unos minutos.")
os.chdir(PROJECT_DIR)

try:
    subprocess.run(["gradle", "assembleDebug"], check=True)
except subprocess.CalledProcessError:
    print("❌ Error al compilar APK. Revisa los logs de Gradle.")
    exit(1)

# Mover APK a Descargas
apk_path = os.path.join(PROJECT_DIR, "app/build/outputs/apk/debug/app-debug.apk")
if os.path.exists(apk_path):
    shutil.copy(apk_path, OUTPUT_DIR)
    print(f"✅ APK generado: {os.path.join(OUTPUT_DIR, 'app-debug.apk')}")
else:
    print("❌ No se encontró el APK generado.")