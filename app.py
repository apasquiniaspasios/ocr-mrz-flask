from flask import Flask, request, render_template, jsonify
from passporteye import read_mrz
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        image = request.files.get('image')
        print("📸 Imagen recibida:", image)

        if image:
            filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            image.save(filepath)
            print("✅ Imagen guardada en:", filepath)

            mrz = read_mrz(filepath)
            print("🔍 Resultado MRZ:", mrz)

            if mrz is not None:
                data = mrz.to_dict()
                print("📄 Datos extraídos:", data)
                return jsonify(success=True, data=data)
            else:
                print("⚠️ MRZ no detectada")
                return jsonify(success=False, error="No se pudo leer la MRZ")

        print("❌ No se recibió ninguna imagen")
        return jsonify(success=False, error="No se recibió imagen")

    except Exception as e:
        print("❌ Error procesando imagen:", e)
        return jsonify(success=False, error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
