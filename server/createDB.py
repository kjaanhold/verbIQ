import csv
import sqlite3

conn = sqlite3.connect('verbIQ.db')
cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS names""")
cur.execute("""CREATE TABLE names (name text)""")

conn.commit()
conn.close()