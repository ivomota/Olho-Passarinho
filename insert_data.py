import sqlite3


location = 'data.db'
table_name = 'IMAGENS'
sql_file = './resultados/insert_data.sql'

conn = sqlite3.connect(location)
c = conn.cursor()

qry = open(sql_file, 'r').read()
sqlite3.complete_statement(qry)

c.executescript(qry)
conn.commit()
c.close()
conn.close()