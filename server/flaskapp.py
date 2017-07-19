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

@app.route('/age/<dob>', methods=['GET'])
def return_age(dob):
    date_object = datetime.strptime(dob, "%Y-%m-%d").date()
    age = date.today() - date_object
    out_text = "Su lapse vanus paevades on: " + str(age.days)
    data = {'messages':[{"text": out_text}]}
    return jsonify(data)

@app.route('/age_block_selection/<dob>', methods=['GET'])
def direct_block_based_on_age(dob):
    date_object = datetime.strptime(dob, "%Y-%m-%d").date()
    age = date.today() - date_object
    data = {"redirect_to_blocks": ["3M_EST"]}
    return jsonify(data)

@app.route("/names/<name>")
def addnames(name):
    con = connect_to_database()
    cur = con.cursor()
    
    query = """INSERT INTO %s VALUES '%s'""" % ('names', name)
    query2 = 'INSERT INTO users VALUES %s' % ('?')

    cur.execute(query2, name)
    
    con.commit()
    cur.close()

    return("Inserted " + str(name) + " to table names")

@app.route("/namelist")
def getnames():
    rows = execute_query("""SELECT * FROM users""")
    return(str(rows))
  
if __name__ == '__main__':
  app.run()