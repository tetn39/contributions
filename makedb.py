import sqlite3

dbname = 'MAIN.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

cur.execute('CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, mention STRING)')

conn.close()