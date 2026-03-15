#!/bin/bash
pkg update -y
pkg install git nodejs npm openjdk-21 unzip wget curl -y
npm install -g cordova
echo "Todo listo. Ahora ejecuta: python server.py"