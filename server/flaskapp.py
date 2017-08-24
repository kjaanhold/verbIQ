 # -*- coding: utf-8 -*-

import csv
import sqlite3
import json
import numpy

from flask import Flask, request, g, jsonify
from datetime import datetime, date
from models import db, Station, TestResults
from sqlalchemy import exc

DATABASE = '/home/ubuntu/verbIQ/server/verbiq.db'

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'my_database',
    'host': 'localhost',
    'port': '5432',
}

app = Flask(__name__)

app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db.init_app(app)

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

@app.route('/', methods = ['GET','POST'])
def hello_world():
    if request.method == "POST":
      lat = request.form['lat']
      lng = request.form['lng']
      new_data = Station(lat=lat, lng=lng)
      db.session.add(new_data)
      db.session.commit()
      return 'OK'
    if request.method == "GET":
      data = Station.query.order_by(Station.id.asc()).first()
      return str(data.lat) + str(data.lng) + str(data.id)

@app.route('/store_test_results', methods = ['GET','POST'])
def store_test_results():
    if request.method == "POST":

      key_user = request.form['messenger user id']
      block_name = request.form['last visited block name']
      lapse_eesnimi = request.form['Lapse_eesnimi']
      date_created = datetime.utcnow()
      result_type = 'chatfuel'
      result_value = request.form['test_result']

      new_data = TestResults(key_user=str(key_user), block_name=str("'"+block_name+"'"), lapse_eesnimi=str(lapse_eesnimi).lower(), date_created=str(date_created), result_type=str(result_type), result_value=str(result_value))
      db.session.add(new_data)
      db.session.commit()
      return 'ok'

    if request.method == "GET":
#      out = TestResults.query.order_by(TestResults.date_created.desc()).first()
      n0 = request.args.get('id_test_result')
      n1 = request.args.get('messenger user id')
      n2 = request.args.get('last visited block id')
      n3 = request.args.get('Lapse_eesnimi')
      n4 = request.args.get('test_result')

      data = {'messages':[{"text": "id_test_result: " + str(n0) + ", " + str(n1) + ", " + str(n2) + ", " + str(n3) + ", " + str(n4)}]}
      return jsonify(data)

def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's 
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return json.dumps(d)



@app.route('/next_test', methods = ['GET','POST'])
def proposenexttest():

    dob = request.args.get('Synni_kuupaev')
    name = request.args.get('Lapse_eesnimi')
    date_object = datetime.strptime(dob, "%Y-%m-%d").date()
    age = date.today() - date_object
    age_months = str(int(age.days)/30)

    if not TestResults.query.filter_by(lapse_eesnimi = name.lower()).first():
      # this kid hasn't done any tests yet
      query = "SELECT t.block_name FROM tests t JOIN milestone_tests ms ON t.id_test = ms.key_test JOIN milestones m ON ms.key_milestone = m.id_milestone WHERE m.target_age <= %s ORDER BY RANDOM() LIMIT 1;" % (age_months)
      text = u"Ei ole veel ühtegi vastust"

    else:
      # this kid has done at least one test
      data = TestResults.query.filter_by(lapse_eesnimi = name.lower()).all()
      result_dict = [u.__dict__ for u in data]
#      out = str(result_dict)
#      out = ['a', 'b']
      out = ["The", "earth", "revolves", "around", "sun"]
      s = str(result_dict[0]['block_name'])
#      out.extend(s)
#      out = "tes"

#      data_str = str(data)

#      data_out = {
#        "block_name": data.block_name,
#        "result_value": data.result_value
#      }

#    json_string = jsonify(data_out)
#    return (data)

    return (out)

'''
      output = {
        'data': TestResults.query.filter_by(lapse_eesnimi = name.lower()).first()
        }
'''

'''
      data_out = {
        "block_name": data.block_name,
        "result_value": data.result_value
      }
      block_name = data.block_name
      result_value = data.result_value

      query = str(block_name)
#      query = "SELECT t.block_name FROM tests t JOIN milestone_tests ms ON t.id_test = ms.key_test JOIN milestones m ON ms.key_milestone = m.id_milestone WHERE m.target_age <= %s AND t.block_name NOT IN (%s) ORDER BY RANDOM() LIMIT 1;" % (age_months, block_name)    
      text = u"Veel vastamata testid"

#    rows = execute_query(query)
    rows = query
    out_text = str(rows)
    out_text = out_text.replace("[(u'","")
    out_text = out_text.replace("',)]","")
#    out_text = str(name)
    data = {
      "redirect_to_blocks": [
        out_text
      ]
    }
    return jsonify(data)
'''


@app.route('/age/', methods=['GET'])
def return_age():
    dob = request.args.get('Synni_kuupaev')
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


@app.route('/age_test_summary', methods=['GET'])
def age_test_summary():
    dob = request.args.get('Synni_kuupaev')
    name = request.args.get('Lapse_eesnimi')
    m4_haarab = request.args.get('4m_haarab')
    m4_refleksid = request.args.get('4m_refleksid')
    m4_seljaltkyljele = request.args.get('4m_seljaltkyljele')
    m4_helisuund = request.args.get('4m_helisuund')
    date_object = datetime.strptime(dob, "%Y-%m-%d").date()
    age = date.today() - date_object
    if (m4_haarab == "Jah" and m4_refleksid == "Jah" and m4_seljaltkyljele == "Jah" and m4_helisuund == "Jah"):
        out_text =  u"Tänan! " + name + u" on omandanud kõik peamised oskused, mida selles vanuses lapse arengu hindamisel jälgitakse: \n 1. blah \n 2. blah-blah\n 3. blah-blah-blah"
    elif (m4_haarab == "Ei" and m4_refleksid == "Ei" and m4_seljaltkyljele == "Ei" and m4_helisuund == "Ei"):
        out_text =  u"Tänan! " + name + u" praegu veel õpib peamisi eakohaseid oskusi: \n 1. blah \n 2. blah-blah\n 3. blah-blah-blah"
    else:
        out_text =  u"Tänan! " + name + u" on juba omandanud järgmised lapse arengus jälgitavad oskused: \n 1. blah \n 2. blah-blah\n 3. blah-blah-blah \n " + name + u" praegu veel õpib neid oskuseid: \n 1. blah \n 2. blah-blah "
    button1 = {
                  "type": "show_block",
                  "block_name": "age_block_selection",
                  "title": u"Default answer"
                }
    button2 =  {
                  "type": "show_block",
                  "block_name": "4,5M_EST",
                  "title": "Viga, parandame..."
                }

    data = {
      "messages": [
        {
          "attachment": {
            "type": "template",
            "payload": {
              "template_type": "button",
              "text": out_text,
              "buttons": [
                button1,
                button2,
                button2
              ]
            }
          }
        }
      ]
    }

    return jsonify(data)

@app.route('/names_check', methods=['GET'])
def names_check():
 #   dob = request.args.get('Synni_kuupaev')
 #   name = request.args.get('Lapse_eesnimi')
    rows = execute_query("""SELECT * FROM names""")
    out_text = str(rows) + "\n"
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
#    elif age_in_days < 6*30:
#        next_block = "4,5M_EST"
    elif age_in_days < 6*30:
        next_block = "next_test_selection"
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
            data = {'messages':[{"text": "Inserted " + str(name) + " to the database \n"}]}
            return jsonify(data)
        except exc.SQLAlchemyError as e:
            reason=str(e)
            data = {'messages':[{"text": reason}]}
            return jsonify(data)
        finally:
            con.close()
    elif request.method == "GET":
        return("This was a GET request")    


@app.route("/age_milestones")
def getmilestones():
    dob = request.args.get('Synni_kuupaev')
    name = request.args.get('Lapse_eesnimi')
    date_object = datetime.strptime(dob, "%Y-%m-%d").date()
    age = date.today() - date_object
    age_months = str(int(age.days)/30)
    query = "SELECT target_age, description FROM milestones WHERE target_age <= %s;" % age_months
    rows = execute_query(query)
    return(str(rows) + "\n")



'''
@app.route("/next_test")
def proposenexttest():

    dob = request.args.get('Synni_kuupaev')
    name = request.args.get('Lapse_eesnimi')
    date_object = datetime.strptime(dob, "%Y-%m-%d").date()
    age = date.today() - date_object
    age_months = str(int(age.days)/30)

    failed_test_two_weeks = "SELECT block_name FROM tests t JOIN test_results tr ON (t.block_name = tr.block_name AND tr.lapse_eesnimi = %s AND m.target_age <= %s AND tr.date_created < date.today() - '2 weeks'::interval) WHERE tr.result_value != '%s' ORDER BY RANDOM() LIMIT 1;" % (name, age, "jah")
    failed_test_two_weeks_rows = execute_query(failed_test_two_weeks)
    failed_test = "SELECT block_name FROM tests t JOIN test_results tr ON (t.block_name = tr.block_name AND tr.lapse_eesnimi = %s AND m.target_age <= %s WHERE tr.result_value != '%s' ORDER BY RANDOM() LIMIT 1;" % (name, age, "jah")
    failed_test_rows = execute_query(failed_test)
    not_answered_older_age_test = "SELECT block_name FROM tests t LEFT JOIN test_results tr ON (t.block_name = tr.block_name AND tr.lapse_eesnimi = %s) WHERE tr.id_test_result IS NULL ORDER BY m.target_age LIMIT 1;" % (name)
    not_answered_older_age_test_rows = execute_query(not_answered_older_age_test)
    if (length(str(not_answered_test_rows))>3):
        next_block_name = str(not_answered_test_rows)
    elif (length(str(failed_test_two_weeks_rows))>3):
        next_block_name = str(failed_test_two_weeks_rows)
    elif (length(str(failed_test_rows))<3):
        next_block_name = str(failed_test_two_weeks_rows)
    elif (length(str(not_answered_older_age_test_rows))>3):
        next_block_name = str(not_answered_older_age_test_rows)
    else:
        next_block_name = "default_answer"
  
    next_block_name = str(not_answered_test_rows) + str(failed_test_two_weeks_rows) + str(not_answered_older_age_test_rows)
    data = {"redirect_to_blocks": [next_block_name]}
#    return jsonify(data)

    return str("test")
'''



'''
@app.route("/test_results")
def test_results():
    dob = request.args.get('Synni_kuupaev')
    name = request.args.get('Lapse_eesnimi')
    date_object = datetime.strptime(dob, "%Y-%m-%d").date()

    age = date.today() - date_object
    age_months = str(int(age.days)/30)

    answered_jah = "SELECT m.description FROM milestones m JOIN milestone_tests mt ON m.id_milestone = mt.key_milestone JOIN tests t on mt.key_test = t.id_test JOIN test_results tr ON (t.block_name = tr.block_name AND tr.lapse_eesnimi = %s AND m.target_age <= %s) WHERE tr.result_value = '%s';" % (name, age_months, "jah")
    answered_ei = "SELECT m.description FROM milestones m JOIN milestone_tests mt ON m.id_milestone = mt.key_milestone JOIN tests t on mt.key_test = t.id_test JOIN test_results tr ON (t.block_name = tr.block_name AND tr.lapse_eesnimi = %s AND m.target_age <= %s) WHERE tr.result_value = '%s';" % (name, age_months, "ei")
    answered_ei_tea = "SELECT m.description FROM milestones m JOIN milestone_tests mt ON m.id_milestone = mt.key_milestone JOIN tests t on mt.key_test = t.id_test JOIN test_results tr ON (t.block_name = tr.block_name AND tr.lapse_eesnimi = %s AND m.target_age <= %s) WHERE tr.result_value = '%s';" % (name, age_months, "ei tea")
 
    # not answered 
    rows_jah = execute_query(answered_jah)
    rows_ei = execute_query(answered_ei)
    rows_ei_tea = execute_query(answered_ei_tea)

    if (length(str(rows_ei)) < 3 and length(str(rows_ei_tea)) < 3 and length(str(rows_jah)) > 2):
        out_text = u"Tänan! " + name + u" on omandanud kõik peamised oskused, mida selles vanuses lapse arengu hindamisel jälgitakse: \n"+ str(rows) + "\n"
    elif (length(str(rows_ei)) > 2 and length(str(rows_ei_tea)) < 3 and length(str(rows_jah)) < 3):
        out_text = u"Tänan! " + name + u" praegu veel õpib peamisi eakohaseid oskusi: \n"+ str(rows_ei) + "\n"
    else:
        out_text = u"Tänan! " + name + u" on juba omandanud järgmised lapse arengus jälgitavad oskused: \n" + str(rows_jah) + "\n" + name + u" õpib praegu veel neid oskuseid: \n" + str(rows_ei) + "\n"

    button1 = {
                  "type": "show_block",
                  "block_name": "age_block_selection",
                  "title": u"Default answer"
                }
    button2 =  {
                  "type": "show_block",
                  "block_name": "4,5M_EST",
                  "title": "Viga, parandame..."
                }

    data = {
      "messages": [
        {
          "attachment": {
            "type": "template",
            "payload": {
              "template_type": "button",
              "text": out_text,
              "buttons": [
                button1,
                button2,
                button2
              ]
            }
          }
        }
      ]
    }

    return jsonify(data)
    '''

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
