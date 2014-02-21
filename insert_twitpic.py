import sqlite3


location = 'data.db'
table_name = 'imagens'
sql_file = './resultados/twitpic_urls.sql'

qry = open(sql_file, 'r').read()
sqlite3.complete_statement(qry)

conn = sqlite3.connect(location)
c = conn.cursor()
c.executescript(qry)
conn.commit()
c.close()
conn.close()