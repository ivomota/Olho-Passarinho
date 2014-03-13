import sqlite3

location = 'data.db'
table_name = 'imagens'

conn = sqlite3.connect(location)
c = conn.cursor()

sql = 'create table if not exists ' + table_name + ' (id integer)'
c.execute(sql)

c.close()
conn.close()
