#!/bin/bash

# Configuración
REPO_NAME="MallyWearApp"
GITHUB_USER="TU_USUARIO_GITHUB"  # Cambia esto por tu usuario de GitHub
GITHUB_TOKEN="TU_TOKEN_PERSONAL" # Cambia esto por tu token de GitHub con permisos

# 1️⃣ Inicializar Git
git init
echo "# $REPO_NAME" > README.md
echo "__pycache__/" > .gitignore
echo "*.apk" >> .gitignore
echo "android_build/" >> .gitignore

git add .
git commit -m "Primer commit: estructura de la app y builder.py"

# 2️⃣ Crear repositorio en GitHub usando API
echo "Creando repo en GitHub..."
curl -u "$GITHUB_USER:$GITHUB_TOKEN" https://api.github.com/user/repos -d "{\"name\":\"$REPO_NAME\"}"

# 3️⃣ Agregar remoto y subir
git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git
git branch -M main
git push -u origin main

echo "✅ Repositorio creado y subido a GitHub: https://github.com/$GITHUB_USER/$REPO_NAME"