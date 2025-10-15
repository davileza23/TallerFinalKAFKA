🧪 Proyecto Final — Kafka + SQLite + Streamlit

Este proyecto demuestra una integración completa entre Kafka, SQLite y Streamlit para la publicación y consumo de datos en tiempo real.

🎯 Objetivo

Crear una base de datos local SQLite con datos de ejemplo (customers).

Publicar las filas como mensajes JSON en un tópico de Kafka.

Consumir y visualizar los mensajes desde una interfaz web hecha en Streamlit.

🏗️ Estructura del proyecto
├── docker-compose.yml / podman-compose.yml   # Contenedores de Kafka, Zookeeper y Kafdrop
├── requirements.txt                          # Librerías necesarias
├── src/
│   ├── create_db.py                          # Crea la base de datos sample.db
│   └── app_streamlit_min.py                  # Interfaz Streamlit con publicación/consumo
├── capturas/                                 # Evidencias del funcionamiento
└── README.md                                 # Este archivo

⚙️ Requisitos previos

Python 3.9+ o superior
WSL Ubuntu (o Linux nativo)
Docker o Podman instalado y en ejecución

🚀 Pasos de ejecución

1️⃣ Levantar Kafka
podman-compose up -d

2️⃣ Crear entorno Python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

3️⃣ Crear base de datos de ejemplo
python src/create_db.py

4️⃣ Ejecutar la interfaz Streamlit
streamlit run src/app_streamlit_min.py


5️⃣ Visualizar

Abrir en el navegador:
👉 http://172.23.164.123:8501
En la pestaña DB → Kafka: publica los datos.
En Consumidor rápido: verifica los mensajes desde el tópico customers_json.


🧩 Tecnologías usadas

Kafka / Zookeeper (Confluent 7.5.0)
SQLite3
Streamlit 1.37+
Python 3.12 (WSL Ubuntu)


📸 Capturas incluidas

Las capturas dentro de la carpeta /capturas muestran:
Interfaz Streamlit corriendo localmente.
Confirmación de Kafka activo en Podman.
Publicación de datos hacia el tópico.
Lectura de mensajes desde el consumidor.


💬 Responsable
Diana Carolina Avilez Avilez
Proyecto académico — Taller Final de Kafka
GitHub: @davileza23
