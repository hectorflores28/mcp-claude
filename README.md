# MCP-Claude

Servidor MCP (Model Context Protocol) para Claude Desktop v1.1.0 (Beta)

## Características

- Protocolo MCP completo (v1.1)
- Sistema de recursos y herramientas
- Rate limiting con Redis
- Caché distribuido con Redis
- Logging de operaciones
- Autenticación JWT y API Key
- Configuración para Claude Desktop
- Tests unitarios y de integración

## Requisitos

- Python 3.8+
- Redis 6.0+
- XAMPP (para desarrollo local)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/mcp-claude.git
cd mcp-claude
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. Iniciar Redis:
```bash
# Asegúrate de que Redis esté instalado y ejecutándose
redis-server
```

6. Iniciar el servidor:
```bash
uvicorn app.main:app --reload
```

## Configuración

### Variables de Entorno

- `SECRET_KEY`: Clave secreta para JWT
- `API_KEY`: Clave API para autenticación
- `REDIS_HOST`: Host de Redis (default: localhost)
- `REDIS_PORT`: Puerto de Redis (default: 6379)
- `REDIS_PASSWORD`: Contraseña de Redis (opcional)
- `REDIS_SSL`: Habilitar SSL para Redis (default: false)

### Claude Desktop

1. Copiar `claude_desktop_config.json` a la carpeta de configuración de Claude Desktop
2. Reiniciar Claude Desktop
3. El protocolo MCP estará disponible automáticamente

## API Endpoints

- `GET /api/mcp/status`: Estado del protocolo MCP
- `POST /api/mcp/execute`: Ejecutar operación MCP
- `GET /api/mcp/operations`: Obtener operaciones recientes

## Desarrollo

### Tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests con cobertura
pytest --cov=app

# Ejecutar tests específicos
pytest tests/unit/test_mcp_service.py
```

### Linting

```bash
# Formatear código
black .

# Ordenar imports
isort .

# Verificar tipos
mypy .
```

## Licencia

MIT

## Contribuir

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request
