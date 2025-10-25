# Sistema de Búsqueda Inteligente con Elasticsearch (MVP)

Este proyecto despliega Elasticsearch + Kibana con Docker y una aplicación Flask
para realizar búsquedas por texto completo, filtros, fuzzy y autocompletado.

## Requisitos
- Docker y Docker Compose instalados
- Python 3.10+

## Pasos rápidos

```bash
# Clonar/descargar este proyecto y entrar a la carpeta
cd elasticsearch-search-system

# 1) Levantar Elasticsearch + Kibana
docker compose up -d

# 2) Crear venv e instalar dependencias
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3) Generar datos + crear índice + indexar
python data/generate_dataset.py
python scripts/create_index.py
python scripts/bulk_index.py

# 4) (opcional) Probar consultas de ejemplo
python scripts/sample_queries.py

# 5) Ejecutar la app web (http://localhost:5001)
python app/app.py
```

