import json, sqlite3, time, random, string
import pandas as pd
import streamlit as st

try:
    from confluent_kafka import Producer, Consumer, KafkaError
    HAS_KAFKA = True
except Exception:
    HAS_KAFKA = False

st.set_page_config(page_title="Kafka Mini Demo", page_icon="🧪", layout="wide")
st.title("🧪 Kafka Mini Demo — DB → Kafka → Consume")

with st.sidebar:
    st.header("Conexión")
    db_path = st.text_input("BD SQLite", "sample.db")
    table = st.text_input("Tabla", "customers")
    bootstrap = st.text_input("Bootstrap", "localhost:9092")
    topic = st.text_input("Topic", "customers_json")
    simulate = st.checkbox("Simular sin Kafka", value=not HAS_KAFKA)

tab_db, tab_mon = st.tabs(["📤 DB → Kafka", "📡 Consumidor rápido"])

with tab_db:
    st.subheader("0) Inicializar BD")
    if st.button("Crear BD demo (3 filas)"):
        try:
            con = sqlite3.connect(db_path)
            con.execute(f"drop table if exists {table}")
            con.execute(f"create table {table}(id integer primary key, name text, city text, amount real)")
            con.executemany(f"insert into {table}(name, city, amount) values(?,?,?)",[
                ("Ana","Bogotá",120.5),("Luis","Medellín",89.0),("Sofía","Cali",150.75)])
            con.commit()
            st.success("BD creada")
        except Exception as e:
            st.error(e)
        finally:
            try: con.close()
            except: pass

    st.subheader("1) Vista de la tabla")
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

    st.subheader("2) Publicación")
    if st.button("Publicar (o simular)"):
        if df.empty:
            st.warning("No hay datos")
        else:
            payloads = df.to_dict(orient="records")
            if simulate or not HAS_KAFKA:
                st.success(f"Simulado: {len(payloads)} mensajes a '{topic}'")
            else:
                p = Producer({"bootstrap.servers": bootstrap})
                for obj in payloads:
                    p.produce(topic, json.dumps(obj, ensure_ascii=False).encode("utf-8"))
                p.flush(10)
                st.success(f"Enviados {len(payloads)} mensajes a '{topic}'")

with tab_mon:
    st.subheader("Consumidor rápido")
    num = st.number_input("Cantidad a leer", 1, 1000, 10)
    from_begin = st.checkbox("Desde el comienzo", True)
    timeout = st.slider("Timeout (s)", 1, 30, 8)
    if st.button("Leer ahora"):
        if not HAS_KAFKA:
            st.error("confluent-kafka no está disponible")
        else:
            gid = "mini-" + "".join(random.choice(string.ascii_lowercase) for _ in range(6))
            conf = {"bootstrap.servers": bootstrap, "group.id": gid, "enable.auto.commit": False,
                    "auto.offset.reset": "earliest" if from_begin else "latest"}
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
                    rows.append({"raw": m.value().decode("utf-8","ignore")})
            c.close()
            if rows:
                st.dataframe(pd.DataFrame(rows), use_container_width=True, height=260)
            else:
                st.info("Sin mensajes")
