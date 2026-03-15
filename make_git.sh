#!/bin/bash

REPO_NAME="MallyWearApp"
GITHUB_USER="TU_USUARIO_GITHUB"  
GITHUB_TOKEN="TU_TOKEN_PERSONAL"

git init
echo "# $REPO_NAME" > README.md
echo "__pycache__/" > .gitignore
echo "*.apk" >> .gitignore
echo "android_build/" >> .gitignore

git add .
git commit -m "Primer commit: estructura de la app y builder.py"

echo "Creando repo en GitHub..."
curl -u "$GITHUB_USER:$GITHUB_TOKEN" https://api.github.com/user/repos -d "{\"name\":\"$REPO_NAME\"}"

git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git
git branch -M main
git push -u origin main

echo "✅ Repositorio creado y subido: https://github.com/$GITHUB_USER/$REPO_NAME"