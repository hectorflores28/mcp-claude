# Guía de Contribución

## Introducción

Gracias por tu interés en contribuir al proyecto MCP-Claude. Este documento proporciona las pautas y el proceso para contribuir al proyecto.

## Requisitos Previos

- Python 3.10+
- Git
- Docker (opcional)
- Redis

## Configuración del Entorno de Desarrollo

1. Clona el repositorio:
```bash
git clone https://github.com/hectorflores28/mcp-claude.git
cd mcp-claude
```

2. Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno:
```bash
cp .env.example .env
# Edita .env con tus configuraciones
```

## Proceso de Desarrollo

1. Crea una rama para tu feature:
```bash
git checkout -b feature/nombre-de-tu-feature
```

2. Realiza tus cambios y commits:
```bash
git add .
git commit -m "feat: descripción de tus cambios"
```

3. Asegúrate de que tus cambios pasen las pruebas:
```bash
pytest
```

4. Ejecuta los linters:
```bash
black .
isort .
flake8 .
mypy .
```

5. Envía un Pull Request:
- Asegúrate de que tu PR tenga una descripción clara
- Incluye tests para nuevas funcionalidades
- Actualiza la documentación según sea necesario

## Estándares de Código

- Seguimos PEP 8 para estilo de código
- Usamos Black para formateo
- Usamos isort para ordenar imports
- Usamos flake8 para linting
- Usamos mypy para verificación de tipos

## Estructura del Proyecto

```
mcp-claude/
├── app/
│   ├── api/          # Endpoints de la API
│   ├── core/         # Funcionalidad central
│   ├── middleware/   # Middleware de FastAPI
│   ├── models/       # Modelos de datos
│   ├── schemas/      # Esquemas Pydantic
│   ├── services/     # Servicios de negocio
│   └── utils/        # Utilidades
├── tests/            # Tests
├── docs/             # Documentación
└── scripts/          # Scripts de utilidad
```

## Testing

- Escribe tests unitarios para nuevas funcionalidades
- Mantén la cobertura de código por encima del 80%
- Usa pytest para testing
- Ejecuta `pytest --cov=app` para ver la cobertura

## Documentación

- Documenta nuevas funcionalidades
- Actualiza el README.md cuando sea necesario
- Mantén actualizada la documentación de la API
- Usa docstrings para documentar funciones y clases

## Proceso de Release

1. Actualiza la versión en `app/core/config.py`
2. Actualiza el CHANGELOG.md
3. Crea un tag de git
4. Genera el release en GitHub

## Contacto

- Abre un issue para preguntas o problemas
- Usa las discusiones de GitHub para debates
- Contacta a los maintainers para temas urgentes

## Licencia

Al contribuir, aceptas que tus contribuciones serán licenciadas bajo la misma licencia que el proyecto. 