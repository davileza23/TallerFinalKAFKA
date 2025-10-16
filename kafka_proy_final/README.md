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
## 3.1 ) Preparar entorno Python
```bash
##para este entorno local pc oficina se Activa entorno virtual en PowerShell (Windows) asi:
.venv\Scripts\Activate
###posterior instalar requeriments.txt
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
```bash
## tener en cuenta que en equipos corporativos el panel tiene mas posibilidad de ejecutarse con el siguiente comando:
##Esto evita ejecutar el binario directamente (streamlit.exe), usando en su lugar el intérprete Python del entorno virtual.
python -m streamlit run app_streamlit.py

```

- Pestaña **DB → Kafka**: crea la BD y publica al tópico (por defecto `customers_json`).
- Pestaña **Consumidor rápido**: lee mensajes del tópico para confirmar.

## 6) Notas
- Cambia `Bootstrap`, `Topic` y ruta de BD desde la barra lateral.

- Tener en cuenta que si en el panel, el confluent-kafka no está disponible (opcion:  Consumidor rápido), se debe detener la app y  volver a iniciar
```bash
python -m streamlit run app_streamlit.py
```
## 6.1) Ajustar podman-compose
- Cambia podman-compose para utilizar desde la maquina corporativa: debido a que en equipos corporativos o con restricciones de red (como proxy, VPN o WSL2), Kafka puede fallar 
- Para resolverlo, se simplificó la configuración de listeners a un único canal PLAINTEXT, eliminando el listener duplicado PLAINTEXT_INTERNAL
- Se dejó solo un listener:
```bash
KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092
KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
```
Se ajustó:
```bash
KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT
```
- Con esto, Kafka inicia correctamente en Podman (Windows/WSL) y acepta conexiones desde Streamlit usando: bootstrap.servers = localhost:9092
