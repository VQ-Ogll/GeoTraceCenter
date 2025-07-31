import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno
load_dotenv()

# Directorio base
BASE_DIR = Path(__file__).parent.resolve()

class Config:
    """Configuración base que heredarán otros entornos"""
    
    # #############################
    # Configuración crítica
    # #############################
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-cambiar-en-produccion')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    
    # #############################
    # Rutas y almacenamiento
    # #############################
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'data')
    BACKUP_FOLDER = os.path.join(BASE_DIR, 'backups')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # #############################
    # Base de datos
    # #############################
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f'sqlite:///{os.path.join(BASE_DIR, "data.db")}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600
    }
    
    # #############################
    # Seguridad
    # #############################
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hora
    
    # #############################
    # API
    # #############################
    API_PREFIX = '/api/v1'
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False  # Desactivar en producción
    
    # #############################
    # Logging
    # #############################
    LOG_FILE = os.path.join(BASE_DIR, 'geotrace.log')
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    @staticmethod
    def init_app(app):
        """Inicialización adicional para la app Flask"""
        # Crear directorios necesarios
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.BACKUP_FOLDER, exist_ok=True)


class DevelopmentConfig(Config):
    """Configuración para desarrollo local"""
    DEBUG = True
    FLASK_ENV = 'development'
    SQLALCHEMY_ECHO = True  # Log de queries SQL
    JSONIFY_PRETTYPRINT_REGULAR = True
    LOG_LEVEL = 'DEBUG'
    
    # Desactivar seguridad para desarrollo
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    LOG_LEVEL = 'CRITICAL'  # Reducir log en tests


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Configuraciones específicas de producción
    PROPAGATE_EXCEPTIONS = False  # No mostrar errores al cliente
    
    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        # Validaciones estrictas en producción
        if not os.getenv('SECRET_KEY'):
            raise ValueError("SECRET_KEY es obligatorio en producción")


# Configuración por entorno
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Obtiene la configuración según el entorno"""
    env = os.getenv('FLASK_ENV', 'production').lower()
    return config.get(env, config['default'])