import csv
import sqlite3

from flask import Flask, request, g, jsonify
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

@app.route('/age')
def return_age(dob):
    date_object = datetime.strptime(dob, "%Y-%m-%d").date()
    age = date.today() - date_object
    return jsonify('age': age.days)

@app.route('/mypage', methods=['GET', 'POST'])
def login():
    name = request.form['name']
    password = request.form['surname']

    return(str(name))

@app.route("/names/<name>")
def addnames(name):
    con = connect_to_database()
    cur = con.cursor()
    
    query = """INSERT INTO %s VALUES '%s'""" % ('names', name)

    #return(str(query))
    cur.execute(query)
    
    #con.commit()
    #con.close()

    #cur.execute(query)
    #g.db.commit()
    #cur.close()
    
    #return("Inserted " + str(name) + " to table names")

@app.route("/namelist")
def getnames():
    rows = execute_query("""SELECT * FROM names""")
    return(str(rows))

if __name__ == '__main__':
    app.run()