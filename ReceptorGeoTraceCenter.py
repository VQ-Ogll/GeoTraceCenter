import os
from flask import Flask, request, jsonify, send_from_directory
from utils.logger import setup_logger
from utils.file_manager import FileManager

app = Flask(__name__)
logger = setup_logger('geotrace')
file_manager = FileManager()

# Configuración básica
app.config['UPLOAD_FOLDER'] = 'data'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

@app.route('/')
def index():
    return send_from_directory('templates', 'dashboard.html')

@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        file_manager.save_data(data)
        logger.info(f"Datos recibidos y almacenados: {data}")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.error(f"Error al procesar datos: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    os.makedirs('backups', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)