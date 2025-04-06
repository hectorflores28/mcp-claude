from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Dict
from app.services.filesystem_service import FileSystemService
from pydantic import BaseModel

router = APIRouter()
filesystem = FileSystemService()

class FileResponse(BaseModel):
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

@router.get("/files", response_model=List[FileResponse])
async def list_files():
    """
    Lista todos los archivos disponibles.
    
    Returns:
        Lista de archivos con sus metadatos
    """
    try:
        return await filesystem.list_files()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al listar archivos: {str(e)}"
        )

@router.get("/files/{filename}", response_model=FileContent)
async def read_file(filename: str):
    """
    Lee el contenido de un archivo específico.
    
    Args:
        filename: Nombre del archivo
        
    Returns:
        Contenido del archivo
    """
    try:
        return await filesystem.read_file(filename)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Archivo no encontrado: {filename}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al leer el archivo: {str(e)}"
        )

@router.post("/files", response_model=FileOperation)
async def create_file(
    filename: str,
    content: str
):
    """
    Crea un nuevo archivo.
    
    Args:
        filename: Nombre del archivo
        content: Contenido del archivo
        
    Returns:
        Información de la operación
    """
    try:
        result = await filesystem.save_file(content, filename)
        return FileOperation(
            filename=result["filename"],
            status="created",
            operation="save",
            timestamp=result["created_at"]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear el archivo: {str(e)}"
        )

@router.delete("/files/{filename}", response_model=FileOperation)
async def delete_file(filename: str):
    """
    Elimina un archivo.
    
    Args:
        filename: Nombre del archivo
        
    Returns:
        Información de la operación
    """
    try:
        result = await filesystem.delete_file(filename)
        return FileOperation(
            filename=result["filename"],
            status=result["status"],
            operation="delete",
            timestamp=result["deleted_at"]
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Archivo no encontrado: {filename}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar el archivo: {str(e)}"
        ) 