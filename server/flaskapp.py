# -*- coding: utf-8 -*-

import csv
import sqlite3

from flask import Flask, request, g, jsonify
from datetime import datetime, date
from sqlalchemy.exc import SQLAlchemyError

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
    out_text = "Selge, su laps on: " + str(age.days) 
    data = {'messages':[{"text": out_text}]}
    return jsonify(data)

@app.route('/age_check', methods=['GET'])
def age_check():
    dob = request.args.get('Synni_kuupaev')
    name = request.args.get('Lapse_eesnimi')
    date_object = datetime.strptime(dob, "%Y-%m-%d").date()
    age = date.today() - date_object
    out_text = u"Tänan. " + (name) + u" sündis " + str(date_object) + " ja ta on praegu " + str(int(round(int(age.days)/30))) + " kuu vanune."
#    out_text = str(dob) + str(name)
#    data = {'messages':[{"text": out_text}]}
    data = {
      "messages": [
        {
          "attachment": {
            "type": "template",
            "payload": {
              "template_type": "button",
              "text": out_text,
              "buttons": [
                {
                  "type": "show_block",
                  "block_name": "age_block_selection",
                  "title": u"Õige, edasi!"
                },
                {
                  "type": "show_block",
                  "block_name": "PARENT_EST",
                  "title": "Viga, parandame..."
                }
              ]
            }
          }
        }
      ]
    }
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

@app.route("/names", methods = ['GET','POST'])
def addnames():
    if request.method == "POST":
        try:
            con = connect_to_database()
            cur = con.cursor()
            name = request.form['name']
            query = "INSERT INTO %s VALUES ('%s');" % ('names', name)
            cur.execute(query)
            con.commit()
            cur.close()
            return("Inserted " + str(name) + " to table names")
        except SQLAlchemyError as e:
            reason=str(e)
            flash(reason)
        
@app.route("/namelist")
def getnames():
    rows = execute_query("""SELECT * FROM names""")
    return(str(rows))
  
if __name__ == '__main__':
  app.run(debug=True)
