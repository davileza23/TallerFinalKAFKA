# Kafka  Project Final — DB → Kafka → Consume (Streamlit)

Proyecto mínimo para entregar un demo funcional:
- SQLite con tabla `customers` y datos ejemplo.
- Publicación de filas como JSON a un tópico Kafka.
- Consumo rápido para verificar los mensajes.

## 1) Requisitos
- WSL Ubuntu / Linux / macOS / Windows con Python 3.9+
- Docker/Docker Compose (o Podman) para Kafka

## 2) Levantar Kafka 
```bash
docker-compose up -d
```
```bash
##levantar kafka con podman-compose
podman-compose up -d
```
```bash
#listarlos
podman ps
```
## 3) Preparar entorno Python
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
```bash
##Comprobar entorno python
pip list
```

## 4) Crear BD de ejemplo
```bash
python create_db.py
```

## 5) Ejecutar el panel
```bash
streamlit run app_streamlit.py
```

- Pestaña **DB → Kafka**: crea la BD y publica al tópico (por defecto `customers_json`).
- Pestaña **Consumidor rápido**: lee mensajes del tópico para confirmar.

## 6) Notas
- Cambia `Bootstrap`, `Topic` y ruta de BD desde la barra lateral.
