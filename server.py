from flask import Flask, request, send_file, send_from_directory
import os, subprocess, uuid

app = Flask(__name__)

@app.route('/')
def home():
    # Esto sirve tu HTML principal
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def style():
    # Sirve el CSS
    return send_from_directory('.', 'style.css')

# --- Rutas que ya tienes ---
@app.route('/generate_from_github', methods=['POST'])
def generate_github():
    data = request.json
    repo_url = data.get('url')
    if not repo_url: return {'success': False, 'error': 'No URL'}, 400

    folder = f"/tmp/{uuid.uuid4()}"
    os.makedirs(folder)
    subprocess.run(['git', 'clone', repo_url, folder])

    app_name = f"App_{uuid.uuid4().hex[:5]}"
    subprocess.run(['cordova', 'create', app_name], cwd=folder)
    subprocess.run(['cordova', 'platform', 'add', 'android'], cwd=os.path.join(folder, app_name))
    subprocess.run(['cordova', 'build', 'android'], cwd=os.path.join(folder, app_name))

    apk_path = os.path.join(folder, app_name, 'platforms', 'android', 'app', 'build', 'outputs', 'apk', 'debug', 'app-debug.apk')
    if not os.path.exists(apk_path):
        return {'success': False, 'error': 'APK no generado'}, 500

    return send_file(apk_path, as_attachment=True)

@app.route('/generate', methods=['POST'])
def generate_upload():
    # Aquí recibirías archivos subidos y los procesas igual que GitHub
    return {'success': False, 'error': 'Función en desarrollo'}, 501

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)