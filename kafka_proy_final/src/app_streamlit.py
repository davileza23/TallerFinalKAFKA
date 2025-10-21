import json, sqlite3, time, random, string
import pandas as pd
import streamlit as st
import smtplib
from email.mime.text import MIMEText

# ============================================
#  K-FLOW INSIGHT
#  Solución educativa para la comprensión y monitoreo 
#  de arquitecturas de mensajería distribuida.
# ============================================

try:
    from confluent_kafka import Producer, Consumer, KafkaError
    HAS_KAFKA = True
except Exception:
    HAS_KAFKA = False

st.title("🧪 K-Flow Insight")
st.caption("Solución educativa para la comprensión y monitoreo de arquitecturas de mensajería distribuida")
st.markdown("---")

# --- PANEL LATERAL ---
with st.sidebar:
    st.header("Conexión")
    db_path = st.text_input("BD SQLite", "KFlowInsight.db")
    table = st.text_input("Tabla", "estudiantes")
    bootstrap = st.text_input("Bootstrap", "localhost:9092")
    topic = st.text_input("Tópico", "estudiantes_json")
    simulate = st.checkbox("Simular sin Kafka", value=not HAS_KAFKA)

# --- TABS PRINCIPALES ---
tab_db, tab_mon = st.tabs(["📤 DB → Kafka", "📡 Lectura en tiempo real"])

# =====================================================
# Envío de correo con HTML y tabla
# =====================================================
def enviar_correo(destinatario, asunto, mensaje, df=None):
    remitente = "carolina.avilez2@gmail.com"
    password = "drvyenqlhdhdgojr"  # token de app Gmail --MiAppKafka

    # Si hay dataframe, se adjunta como HTML
    if df is not None and not df.empty:
        mensaje += "<br><br><b>Últimos mensajes consumidos:</b><br>"
        mensaje += df.head(10).to_html(index=False, border=1)

    msg = MIMEText(mensaje, "html")
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destinatario

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(remitente, password)
            server.send_message(msg)
        return True
    except Exception as e:
        print("Error al enviar correo:", e)
        return False

# =====================================================
# TAB 1: PUBLICADOR (SQLite → Kafka)
# =====================================================
with tab_db:
    st.subheader("0) Inicializar Base de Datos")
    if st.button("Crear BD (3 filas)"):
        try:
            con = sqlite3.connect(db_path)
            con.execute(f"drop table if exists {table}")
            con.execute(f"create table {table}(id integer primary key, nombre text, curso text, promedio real)")
            con.executemany(
                f"insert into {table}(nombre, curso, promedio) values(?,?,?)",
                [("Ana Suarez","cuarto",90.5), ("Luis Lopez","primero",89.0), ("Sofía Martinez","segundo",75.8)]
            )
            con.commit()
            st.success("Base de datos creada exitosamente.")
        except Exception as e:
            st.error(e)
        finally:
            try: con.close()
            except: pass

    st.subheader("1) Visualización de la tabla actual")
    try:
        con = sqlite3.connect(db_path)
        df = pd.read_sql_query(f"select * from {table}", con)
        st.dataframe(df, use_container_width=True, height=250)
    except Exception as e:
        st.info("Crea la BD primero")
        df = pd.DataFrame()
    finally:
        try: con.close()
        except: pass

    st.subheader("2) Publicar registros como mensajes JSON")
    if st.button("Publicar (o simular envío)"):
        if df.empty:
            st.warning("No hay datos para publicar")
        else:
            payloads = df.to_dict(orient="records")
            if simulate or not HAS_KAFKA:
                st.success(f"Modo educativo: simulación de envío de {len(payloads)} mensajes a '{topic}'")
            else:
                p = Producer({"bootstrap.servers": bootstrap})
                for obj in payloads:
                    p.produce(topic, json.dumps(obj, ensure_ascii=False).encode("utf-8"))
                p.flush(10)
                st.success(f"Enviados {len(payloads)} mensajes reales a '{topic}'")

# =====================================================
# TAB 2: CONSUMIDOR (Kafka → Streamlit)
# =====================================================
with tab_mon:
    st.subheader("Monitor de consumo en tiempo real")
    st.write("Lee y visualiza mensajes publicados en el tópico de Kafka.")

    num = st.number_input("Cantidad de mensajes a leer", 1, 1000, 10)
    from_begin = st.checkbox("Leer desde el inicio del tópico", True)
    timeout = st.slider("Tiempo máximo de espera (segundos)", 1, 30, 8)

    if st.button("Leer ahora"):
        if not HAS_KAFKA:
            st.error("Librería confluent-kafka no disponible.")
        else:
            gid = "mini-" + "".join(random.choice(string.ascii_lowercase) for _ in range(6))
            conf = {
                "bootstrap.servers": bootstrap,
                "group.id": gid,
                "enable.auto.commit": False,
                "auto.offset.reset": "earliest" if from_begin else "latest"
            }
            c = Consumer(conf)
            c.subscribe([topic])
            rows = []
            deadline = time.time() + timeout
            while len(rows) < num and time.time() < deadline:
                m = c.poll(0.5)
                if m is None: continue
                if m.error():
                    if m.error().code() == KafkaError._PARTITION_EOF: continue
                    else: st.error(str(m.error())); break
                try:
                    rows.append(json.loads(m.value().decode("utf-8")))
                except Exception:
                    rows.append({"raw": m.value().decode("utf-8", "ignore")})
            c.close()

            if rows:
                st.session_state["df_cons"] = pd.DataFrame(rows)  # 👈 guardamos en sesión
                st.success(f"Recibidos {len(rows)} mensajes desde '{topic}'")
            else:
                st.info("No se recibieron mensajes en el tiempo establecido.")

    # --- Mostrar DataFrame si existe ---
    if "df_cons" in st.session_state:
        df_cons = st.session_state["df_cons"]
        st.dataframe(df_cons, use_container_width=True, height=260)

        # --- CORREO SOLO AQUÍ ---
        st.markdown("---")
        st.subheader("📧 Enviar correo con los datos recibidos")
        email = st.text_input("Correo electrónico", placeholder="tu.correo@ejemplo.com")

        if st.button("Enviar correo con datos"):
            if email:
                exito = enviar_correo(
                    email,
                    "Resumen Kafka",
                    "Mensajes más recientes recibidos en Kafka",
                    df=df_cons
                )
                if exito:
                    st.success(f"Correo enviado a {email}")
                else:
                    st.error("Error al enviar el correo.")
            else:
                st.warning("Por favor, ingresa un correo válido.")
