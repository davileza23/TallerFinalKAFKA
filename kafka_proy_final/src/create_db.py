import sqlite3
con = sqlite3.connect("KFlowInsight.db")
con.execute("drop table if exists estudiantes")
con.execute("create table estudiantes(id integer primary key, nombre text, curso text, promedio real)")
con.executemany("insert into estudiantes(nombre, curso, promedio) values(?,?,?)",[ ("Ana Suarez","cuarto",90.5), ("Luis Lopez","primero",89.0), ("Sofía Martinez","segundo",75.8),])
con.commit(); con.close()
print("OK: creada KFlowInsight.db con 3 filas en estudiantes")