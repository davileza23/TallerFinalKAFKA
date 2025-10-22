🧪 Proyecto Final — Kafka + SQLite + Streamlit

Aplicación (py) que permite visualizar, enviar y consumir mensajes en tiempo real desde Apache Kafka, utilizando una base de datos SQLite como fuente de datos.
Incluye un módulo de notificación por correo que envía los resultados del consumo directamente al usuario.



🎯 Objetivo
Facilitar la comprensión y observación del funcionamiento de Kafka como sistema de mensajería distribuida, ofreciendo una herramienta práctica y educativa para monitorear el flujo de información entre productores y consumidores en tiempo real.

🏗️ Estructura del proyecto 
```
kafka_proy_final/
├── docker-compose.yml           # (opcional, no usado en Podman)
├── podman-compose.yml           # Servicios Kafka + Zookeeper + Kafdrop
├── requirements.txt             # Dependencias de Python
├── README.md                    # Instrucciones del proyecto
├── src/
│   ├── app_streamlit.py         # Interfaz principal (DB → Kafka → Consumo)
│   ├── create_db.py             # Script para crear sample.db con 3 filas
│   └── sample.db                # Base de datos SQLite generada
└── capturas/                    # Evidencias del funcionamiento - archivo word

```


⚙️ Requisitos previos

Python 3.9+ o superior WSL Ubuntu (o Linux nativo) Docker o Podman instalado y en ejecución


🚀 Pasos de ejecución

Levantar Kafka
```
docker-compose up -d
##levantar kafka con podman-compose
podman-compose up -d
#listarlos
podman ps
```
Preparar entorno Python
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
##Comprobar entorno python
pip list
```
Abrir en el navegador: 👉 http://172.23.164.123:8501 En la pestaña DB → Kafka: publica los datos. En Consumidor rápido: verifica los mensajes desde el tópico customers_json.


🧩 Tecnologías usadas

Kafka / Zookeeper /kafdrop (Confluent 7.5.0) SQLite3 Streamlit 1.37+ Python 3.12 (WSL Ubuntu)


📸 Evidencias

Las capturas se encuentran dentro de la carpeta /capturas del proyecto (kafka_proy_final) esta alojado un documento de word que muestra el paso a paso de actividades realizadas, allí se evidencian la Interfaz Streamlit corriendo localmente. Confirmación de Kafka activo en Podman. Publicación de datos hacia el tópico y Lectura de mensajes desde el consumidor.


💬 Responsable:
```
Diana Carolina Avilez Avilez
Taller Final de Kafka Universidad Santo Tomás/DIAN
GitHub: @davileza23
```
## Autor(a)

- [@davileza23](https://github.com/davileza23/TallerFinalKAFKA)


## Documentación

[Evidencias ejecución proyecto final](https://github.com/davileza23/TallerFinalKAFKA/blob/main/kafka_proy_final/capturas/ProyectoFinalKafka.docx)

