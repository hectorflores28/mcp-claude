from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class FileMetadata(BaseModel):
    filename: str
    size: int
    created_at: str
    mime_type: str

class FileContent(BaseModel):
    filename: str
    content: str
    size: int
    mime_type: str

class FileOperation(BaseModel):
    filename: str
    status: str
    operation: str
    timestamp: str

class FileCreateRequest(BaseModel):
    filename: str = Field(..., description="Nombre del archivo a crear")
    content: str = Field(..., description="Contenido del archivo")
    format_type: Optional[str] = Field("article", description="Tipo de formato para archivos Markdown")

class FileReadRequest(BaseModel):
    filename: str = Field(..., description="Nombre del archivo a leer")

class FileDeleteRequest(BaseModel):
    filename: str = Field(..., description="Nombre del archivo a eliminar")

class FileSystemToolSchema(BaseModel):
    name: str = "filesystem"
    description: str = "Operaciones CRUD en el sistema de archivos"
    parameters: Dict = {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string", 
                "description": "Operación a realizar (create, read, list, delete)",
                "enum": ["create", "read", "list", "delete"]
            },
            "filename": {"type": "string", "description": "Nombre del archivo"},
            "content": {"type": "string", "description": "Contenido del archivo (para create)"}
        },
        "required": ["operation"]
    } 