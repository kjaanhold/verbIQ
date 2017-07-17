import csv
import sqlite3

from flask import Flask, request, g
from datetime import datetime, date

DATABASE = '/home/ubuntu/verbIQ/verbiq.db'
app = Flask(__name__)
app.config.from_object(__name__)

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/age/<dob>', methods=['GET'])
def return_age(dob):
    date_object = datetime.strptime(dob, "%Y-%m-%d").date()
    age = date.today() - date_object
    return("Your age is " + str(age.days) + " days")

@app.route("/names/<name>")
def addnames(name):
    query = """INSERT INTO names VALUES ?"""
    rows = execute_query(query, name.title())
    return("Inserted " + str(rows) + " to table names")

@app.route("/namelist")
def getnames():
    rows = execute_query("""SELECT * FROM names""")
    return(str(rows))
  
if __name__ == '__main__':
  app.run()