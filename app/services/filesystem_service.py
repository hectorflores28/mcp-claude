import os
import aiofiles
from typing import List, Dict, Optional
from datetime import datetime
from app.core.config import settings
import magic
import json
from pathlib import Path

class FileSystemService:
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        self.log_dir = settings.LOG_DIR
        self.max_file_size = settings.MAX_FILE_SIZE
        self.allowed_extensions = settings.ALLOWED_EXTENSIONS
        
        # Crear directorios si no existen
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)
    
    def _get_file_path(self, filename: str) -> str:
        """Obtiene la ruta completa del archivo."""
        return os.path.join(self.upload_dir, filename)
    
    def _get_log_path(self, filename: str) -> str:
        """Obtiene la ruta completa del archivo de log."""
        return os.path.join(self.log_dir, filename)
    
    def _is_allowed_extension(self, filename: str) -> bool:
        """Verifica si la extensión del archivo está permitida."""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    async def save_file(self, content: str, filename: str) -> Dict:
        """
        Guarda un archivo en el sistema.
        
        Args:
            content: Contenido del archivo
            filename: Nombre del archivo
            
        Returns:
            Dict con información del archivo guardado
        """
        if not self._is_allowed_extension(filename):
            raise ValueError(f"Extensión no permitida. Permitidas: {', '.join(self.allowed_extensions)}")
        
        file_path = self._get_file_path(filename)
        
        try:
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(content)
            
            # Registrar la operación
            await self.log_operation("save", filename, len(content))
            
            return {
                "filename": filename,
                "path": file_path,
                "size": len(content),
                "created_at": datetime.now().isoformat()
            }
        except Exception as e:
            raise Exception(f"Error al guardar el archivo: {str(e)}")
    
    async def read_file(self, filename: str) -> Dict:
        """
        Lee un archivo del sistema.
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            Dict con el contenido del archivo
        """
        file_path = self._get_file_path(filename)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {filename}")
        
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            # Registrar la operación
            await self.log_operation("read", filename, len(content))
            
            return {
                "filename": filename,
                "content": content,
                "size": len(content),
                "mime_type": magic.from_file(file_path, mime=True)
            }
        except Exception as e:
            raise Exception(f"Error al leer el archivo: {str(e)}")
    
    async def list_files(self) -> List[Dict]:
        """
        Lista todos los archivos en el directorio de uploads.
        
        Returns:
            Lista de archivos con sus metadatos
        """
        files = []
        for filename in os.listdir(self.upload_dir):
            if self._is_allowed_extension(filename):
                file_path = self._get_file_path(filename)
                files.append({
                    "filename": filename,
                    "size": os.path.getsize(file_path),
                    "created_at": datetime.fromtimestamp(
                        os.path.getctime(file_path)
                    ).isoformat(),
                    "mime_type": magic.from_file(file_path, mime=True)
                })
        return files
    
    async def log_operation(
        self,
        operation: str,
        filename: str,
        size: int,
        additional_info: Optional[Dict] = None
    ) -> None:
        """
        Registra una operación en el archivo de log.
        
        Args:
            operation: Tipo de operación (save, read, etc.)
            filename: Nombre del archivo
            size: Tamaño del archivo
            additional_info: Información adicional (opcional)
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "filename": filename,
            "size": size,
            "additional_info": additional_info or {}
        }
        
        log_file = self._get_log_path("filesystem.log")
        try:
            async with aiofiles.open(log_file, 'a', encoding='utf-8') as f:
                await f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"Error al registrar operación: {str(e)}")
    
    async def delete_file(self, filename: str) -> Dict:
        """
        Elimina un archivo del sistema.
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            Dict con información de la operación
        """
        file_path = self._get_file_path(filename)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {filename}")
        
        try:
            os.remove(file_path)
            
            # Registrar la operación
            await self.log_operation("delete", filename, 0)
            
            return {
                "filename": filename,
                "status": "deleted",
                "deleted_at": datetime.now().isoformat()
            }
        except Exception as e:
            raise Exception(f"Error al eliminar el archivo: {str(e)}") 