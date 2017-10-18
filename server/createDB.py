import csv
import sqlite3

conn = sqlite3.connect('verbiq.db')
cur = conn.cursor()

fp = open('/home/ubuntu/verbIQ/server/verbiq_schema.sql', 'r')
data = fp.read().decode("utf-8-sig").encode("utf-8").replace('\n', '').replace('\t','')
data = data.split(";")

for query in data:
	cur.execute(query)

fp = open('/home/ubuntu/verbIQ/server/fill_milestone_tests_table.sql', 'r')
data = fp.read().decode("utf-8-sig").encode("utf-8").replace('\n', '').replace('\t','')
data = data.split(";")

for query in data:
	cur.execute(query)

fp = open('/home/ubuntu/verbIQ/server/fill_tests_table.sql', 'r')
data = fp.read().decode("utf-8-sig").encode("utf-8").replace('\n', '').replace('\t','')
data = data.split(";")

for query in data:
	cur.execute(query)

fp = open('/home/ubuntu/verbIQ/server/fill_milestones_table.sql', 'r')
data = fp.read().decode("utf-8-sig").encode("utf-8").replace('\n', '').replace('\t','')
data = data.split(";")

for query in data:
	cur.execute(query)

fp = open('/home/ubuntu/verbIQ/server/fill_exercises_table.sql', 'r')
data = fp.read().decode("utf-8-sig").encode("utf-8").replace('\n', '').replace('\t','')
data = data.split(";")

for query in data:
	cur.execute(query)

fp = open('/home/ubuntu/verbIQ/server/fill_milestones_exercises_table.sql', 'r')
data = fp.read().decode("utf-8-sig").encode("utf-8").replace('\n', '').replace('\t','')
data = data.split(";")

for query in data:
	cur.execute(query)

conn.commit()
conn.close()