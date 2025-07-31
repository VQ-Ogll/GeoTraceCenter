import os
from flask import Flask, request, jsonify, send_from_directory
from utils.logger import setup_logger
from utils.file_manager import FileManager
from config import get_config  # Nueva importación
from flask_talisman import Talisman  # Seguridad HTTPS
from flask_cors import CORS  # Manejo CORS

# Configuración inicial
app = Flask(__name__)
app.config.from_object(get_config())  # Cargar configuración desde config.py

# Seguridad
Talisman(app, content_security_policy=None)  # Configura CSP según necesidades
CORS(app, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS', '*')}})

# Inicialización de componentes
logger = setup_logger('geotrace')
file_manager = FileManager()

@app.route('/')
def index():
    """Endpoint principal que sirve el dashboard"""
    return send_from_directory('templates', 'dashboard.html')

@app.route('/api/v1/data', methods=['POST'])
def receive_data():
    """
    Endpoint para recibir datos de geolocalización
    Ejemplo de payload:
    {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "timestamp": "2023-01-01T12:00:00Z",
        "device_id": "unique-device-123"
    }
    """
    required_fields = ['latitude', 'longitude', 'timestamp']
    
    # Validación básica
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
        
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    # Validación de campos obligatorios
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing": missing_fields
        }), 400
    
    try:
        # Procesamiento de datos
        file_manager.save_data(data)
        logger.info("Data received", extra={
            "data": data,
            "client_ip": request.remote_addr
        })
        
        return jsonify({
            "status": "success",
            "received": data
        }), 201
        
    except Exception as e:
        logger.error("Data processing failed", exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    """Servir archivos estáticos"""
    return send_from_directory('static', filename)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.critical("Server error", exc_info=True)
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Crear directorios necesarios
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['BACKUP_FOLDER'], exist_ok=True)
    
    # Ejecutar servidor
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=app.config['DEBUG']
    )
