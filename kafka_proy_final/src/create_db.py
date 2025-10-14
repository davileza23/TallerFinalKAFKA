import sqlite3
con = sqlite3.connect("sample.db")
con.execute("drop table if exists customers")
con.execute("create table customers(id integer primary key, name text, city text, amount real)")
con.executemany("insert into customers(name, city, amount) values(?,?,?)",[
    ("Ana","Bogotá",120.5),
    ("Luis","Medellín",89.0),
    ("Sofía","Cali",150.75),
])
con.commit(); con.close()
print("OK: creada sample.db con 3 filas en customers")
