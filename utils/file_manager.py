import json
import os
from datetime import datetime

class FileManager:
    def __init__(self):
        self.data_dir = 'data'
        self.backup_dir = 'backups'
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

    def save_data(self, data):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.data_dir}/trazas.json"
        backup_filename = f"{self.backup_dir}/trazas_{timestamp}.json"
        
        # Guardar datos principales
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        
        # Crear backup
        with open(backup_filename, 'w') as f:
            json.dump(data, f, indent=4)