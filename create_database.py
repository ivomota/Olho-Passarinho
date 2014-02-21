import sqlite3

location = 'data.db'
table_name = 'imagens'

conn = sqlite3.connect(location)
c = conn.cursor()

# Create table
sql = 'create table if not exists ' + table_name + ' (id integer PRIMARY KEY AUTOINCREMENT, id_objeto text, servico text, url text, tipo text, retweet text)'
c.execute(sql)

c.close()
conn.close()