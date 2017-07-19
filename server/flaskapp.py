import csv
import sqlite3

from flask import Flask, request, g, jsonify
from datetime import datetime, date

DATABASE = '/home/ubuntu/verbIQ/server/verbiq.db'
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

@app.route('/age_months/<dob>', methods=['GET'])
def return_age_in_months(dob):
    date_object = datetime.strptime(dob, "%Y-%m-%d").date()
    age = date.today() - date_object
    out_text = round(int(age.days)/30)
    data = {"set_attributes":{"Vanus_kuudes":out_text},"block_names":["PARENT_EST"],"type":"show_block","title":"go"}
    return jsonify(data)

@app.route('/age_block_selection/<dob>', methods=['GET'])
def direct_block_based_on_age(dob):
    date_object = datetime.strptime(dob, "%Y-%m-%d").date()
    age = date.today() - date_object
    age_in_days = int(age.days)
    if age_in_days < 3*30:
        next_block = "2M_EST"
    elif age_in_days < 4.5*30:
        next_block = "3M_EST"        
    elif age_in_days < 6*30:
        next_block = "4,5M_EST"
    elif age_in_days < 7*30:
        next_block = "6M_EST"
    elif age_in_days < 8*30:
        next_block = "7M_EST"
    elif age_in_days < 9*30:
        next_block = "8M_EST"
    elif age_in_days < 12*30:
        next_block = "9M_EST"
    elif age_in_days < 1.5*365:
        next_block = "12M_EST"
    elif age_in_days < 2*365:
        next_block = "18M_EST"
    elif age_in_days < 3*365:
        next_block = "24M_EST"
    elif age_in_days < 4*365:
        next_block = "36M_EST"
    else:
        next_block = "48M_EST"
    data = {"redirect_to_blocks": [next_block]}
    return jsonify(data)

@app.route("/names/<name>")
def addnames(name):
    con = connect_to_database()
    cur = con.cursor()
    
    query = "INSERT INTO %s VALUES ('%s')" % ('names', name)
    
    cur.execute(query)
    con.commit()
    cur.close()

    return("Inserted " + str(name) + " to table names")

@app.route("/namelist")
def getnames():
    rows = execute_query("""SELECT * FROM names""")
    return(str(rows))
  
if __name__ == '__main__':
  app.run()