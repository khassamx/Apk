from flask import Flask, request, send_file, render_template_string
import subprocess, os, uuid, shutil

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Generador de APK desde GitHub</title>
<style>
body{font-family:Arial;background:#111;color:#fff;text-align:center;padding:50px;}
input[type=text]{padding:10px;margin:10px;width:300px;}
button{padding:10px 20px;margin:10px;cursor:pointer;background:#28a745;color:#fff;border:none;border-radius:5px;}
button:hover{background:#218838;}
p{margin:10px 0;}
</style>
</head>
<body>
<h1>Convierte tu GitHub en APK</h1>
<p>Pega el enlace de tu repositorio y genera tu APK</p>
<input type="text" id="repo_url" placeholder="https://github.com/khassamx/tycoon">
<button onclick="generateGitHub()">Generar APK</button>
<p id="status"></p>
<script>
async function generateGitHub(){
    const url = document.getElementById('repo_url').value;
    document.getElementById('status').innerText='Generando APK... ⏳';
    const res = await fetch('/generate_from_github',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({url})
    });
    if(res.status===200){
        const blob = await res.blob();
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'app.apk';
        a.click();
        document.getElementById('status').innerText='APK generado ✅';
    } else {
        const data = await res.json();
        document.getElementById('status').innerText='Error: '+data.error;
    }
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/generate_from_github', methods=['POST'])
def generate_github():
    data = request.json
    repo_url = data.get('url')
    if not repo_url:
        return {'error':'No URL provided'}, 400

    tmp_folder = f"/data/data/com.termux/files/home/tmp_{uuid.uuid4().hex[:6]}"
    os.makedirs(tmp_folder)
    try:
        # 1️⃣ Clonar el repo
        subprocess.run(['git','clone',repo_url,tmp_folder], check=True)

        # 2️⃣ Crear proyecto Cordova
        app_name = f"MyApp_{uuid.uuid4().hex[:5]}"
        app_folder = os.path.join(tmp_folder, app_name)
        subprocess.run(['cordova','create',app_name], cwd=tmp_folder, check=True)

        # 3️⃣ Copiar archivos HTML/CSS/JS al www
        www_folder = os.path.join(app_folder,'www')
        for file in os.listdir(tmp_folder):
            src = os.path.join(tmp_folder,file)
            if os.path.isfile(src) and file.endswith(('.html','.css','.js')):
                shutil.copy(src,www_folder)

        # 4️⃣ Agregar Android y compilar
        subprocess.run(['cordova','platform','add','android'], cwd=app_folder, check=True)
        subprocess.run(['cordova','build','android'], cwd=app_folder, check=True)

        # 5️⃣ Devolver APK
        apk_path = os.path.join(app_folder,'platforms','android','app','build','outputs','apk','debug','app-debug.apk')
        if not os.path.exists(apk_path):
            return {'error':'APK no generado'}, 500

        return send_file(apk_path, as_attachment=True)

    except subprocess.CalledProcessError as e:
        return {'error':str(e)}, 500
    finally:
        shutil.rmtree(tmp_folder, ignore_errors=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)