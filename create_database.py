import sqlite3

location = 'data.db'
table_name = 'IMAGENS'

conn = sqlite3.connect(location)
c = conn.cursor()

# Create table
sql = 'create table if not exists ' + table_name + ' (id integer PRIMARY KEY AUTOINCREMENT, id_tweet text, servico text, url text, tipo text, retweet text)'
c.execute(sql)

c.close()
conn.close()