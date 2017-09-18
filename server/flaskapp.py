# -*- coding: utf-8 -*-
import csv
import sqlite3
import json
import math
# import scipy

from flask import Flask, request, g, jsonify, Response
from datetime import datetime, date
from models import db, Station, TestResults, Test, MilestoneTests
from sqlalchemy import exc
from sqlalchemy.orm.exc import NoResultFound


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
'''
@app.route('/', methods = ['GET','POST'])
def hello_world():
    if request.method == "POST":
      lat = request.form['lat']
      lng = request.form['lng']
      last_updated = datetime.utcnow()

      new_data = Station(lat=lat, lng=lng, last_updated=last_updated)
      db.session.add(new_data)
      db.session.commit()
      return 'OK'
    if request.method == "GET":
      data = Station.query.order_by(Station.id.asc()).first()
      return str(data.lat) + str(data.lng) + str(data.id)
'''

@app.route('/store_test_results', methods = ['GET','POST'])
def store_test_results():
    if request.method == "POST":
      key_user = request.form['messenger user id']
      block_name = request.form['last_visited_block_id']
      lapse_eesnimi = request.form['Lapse_eesnimi']
      date_created = datetime.utcnow()
      result_type = 'chatfuel'
      result_value = request.form['test_result']

      new_data = TestResults(key_user=str(key_user), block_name=str("'"+block_name+"'"), lapse_eesnimi=str(lapse_eesnimi.encode('utf8')).lower(), date_created=str(date_created), result_type=str(result_type), result_value=str(result_value))
      db.session.add(new_data)
      db.session.commit()

      data = {"redirect_to_blocks": ["test recurring tests 2"]}
      return jsonify(data)

    if request.method == "GET":
#      out = TestResults.query.order_by(TestResults.date_created.desc()).first()
      n1 = request.args.get('messenger user id')
      n2 = request.args.get('last_visited_block_id')
      n3 = request.args.get('Lapse_eesnimi')
      n4 = request.args.get('test_result')

      data = {'messages':[{"text": "id_test_result: " + " / " + str(n1) + " / "  + ", " + str(n2) + " / "  + ", " + str(n3) + " / " + ", " + str(n4)}]}
      return jsonify(data)



@app.route('/store_children', methods = ['GET','POST'])
def store_children():
    if request.method == "POST":
      key_user = request.form['messenger user id']
      lapse_eesnimi = request.form['Lapse_eesnimi']
      date_of_birth = request.form['Synni_kuupaev']
      gender = request.form['Lapse_sugu']
      first_updated = datetime.utcnow()
      last_updated = datetime.utcnow()

      new_data = Children(key_user=str(key_user), lapse_eesnimi=str(lapse_eesnimi.encode('utf8')).lower(), date_of_birth=str(date_of_birth), gender=str(gender), first_updated=str(first_updated), last_updated=str(last_updated))

      db.session.add(new_data)
      db.session.commit()

      data = {"redirect_to_blocks": ["test recurring tests 2"]}
      return jsonify(data)

    if request.method == "GET":
      data = {'messages':[{"text": "error: "}]}
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


#@app.route('/next_test_selection', methods=['GET'])
def next_test_selection(dob,name):
#def next_test_selection():
#    dob = request.args.get('Synni_kuupaev')
#    name = request.args.get('Lapse_eesnimi')

    date_object = datetime.strptime(dob, "%Y-%m-%d").date()
    age = date.today() - date_object
    age_months = str(int(age.days)/30)

      # this kid hasn't done any tests yet
    if TestResults.query.filter_by(lapse_eesnimi = name.lower()).first() is None:

      query = "SELECT t.description, t.block_name FROM tests t JOIN milestone_tests ms ON t.id_test = ms.key_test JOIN milestones m ON ms.key_milestone = m.id_milestone WHERE m.target_age BETWEEN (2*%s)/3 AND (4*%s)/3 ORDER BY RANDOM() LIMIT 1;" % (age_months, age_months)
      rows = execute_query(query)

      question = str(rows[0][0].encode("utf-8"))
      block_name = str(rows[0][1].encode("utf-8"))

    else:
      # this kid has done at least one test
      data = TestResults.query.filter_by(lapse_eesnimi = name.lower()).all()
      result_dict = [u.__dict__ for u in data]
      block_name = [d.get('block_name') for d in result_dict]
      block_name = str(block_name)
      block_name = block_name.replace('u"','')
      block_name = block_name.replace('"','')
#      block_name = block_name.replace("u'","'")
      block_name = block_name.replace('[','')
      block_name = block_name.replace(']','')
 
      query = "SELECT t.description, t.block_name FROM tests t JOIN milestone_tests ms ON t.id_test = ms.key_test JOIN milestones m ON ms.key_milestone = m.id_milestone WHERE ( m.target_age BETWEEN (2*%s)/3 AND (4*%s)/3 ) AND t.block_name NOT IN (%s) ORDER BY RANDOM() LIMIT 1;" % (age_months, age_months, block_name)    

      rows = execute_query(query)

      if str(rows) == '[]':
        question  = 'done'
        block_name = 'test_summary'

      else:
        question = str(rows[0][0].encode("utf-8"))
        block_name = str(rows[0][1].encode("utf-8"))

    return str(question) + '///' + str(block_name)





@app.route('/run_test', methods=['GET'])
def run_test():
    dob = request.args.get('Synni_kuupaev')
    name = request.args.get('Lapse_eesnimi')

    selected_test = next_test_selection(dob = dob, name = name)

    question = str(selected_test.split("///")[0])
    block_name = str(selected_test.split("///")[1])
    data = str(question) + "//" + str(block_name)

    if question == "done":
      data = {"redirect_to_blocks": [block_name]}

    else:
      data = {
        "set_attributes":
          {
            "last_visited_block_id": block_name
          },
        "messages": [
          {
            "attachment": {
              "type": "template",
              "payload": {
                "template_type": "button",
                "text": question.decode("utf-8"),
                "buttons": [
                  {
                    "set_attributes": 
                    {
                      "test_result": "Jah"
                    },
                    "type": "show_block",
                    "block_name": "test recurring tests 3",
                    "title": u"Jah"
                  },
                  {
                    "set_attributes": 
                    {
                      "test_result": "Ei tea"
                    },
                    "type": "show_block",
                    "block_name": "test recurring tests 3",
                    "title": u"Ei tea"
                  },                
                  {
                    "set_attributes": 
                    {
                      "test_result": "Ei"
                    },
                    "type": "show_block",
                    "block_name": "test recurring tests 3",
                    "title": u"Ei"
                  }
                ]
              }
            }
          }
        ]
      }      

    response = Response(json.dumps(data,ensure_ascii = False), content_type="application/json; charset=utf-8")
    return response





@app.route('/lognorm', methods=['GET'])
def lognorm():
  x = float(request.args.get('x'))  
  mean = float(request.args.get('mean'))  
  var = float(request.args.get('var'))  

  mu = float(math.log((mean**2) / math.sqrt(var + mean**2) ))
  sigma = float(math.sqrt(math.log(var / mean**2 + 1)))
  a = (math.log(x) - mu)/math.sqrt(2*sigma**2)
  p = 0.5 + 0.5*math.erf(a)

  return str(p)

@app.route('/pg_data', methods=['GET'])
def pg_data():
  test = db.session.query(Test, MilestoneTests).one()
  result_dict = [u.__dict__ for u in test]
  block_name = [d.get('block_name') for d in result_dict]    
  return(str(block_name[0]))

@app.route('/age_check', methods=['GET'])
def age_check():
    dob = request.args.get('Synni_kuupaev')
    name = request.args.get('Lapse_eesnimi')
    date_object = datetime.strptime(dob, "%Y-%m-%d").date()
    age = date.today() - date_object
    out_text = u"Tänan. " + (name) + u" sündis " + str(date_object) + " ja ta on praegu " + str(int(round(int(age.days)/30))) + " kuu vanune."
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
                  "block_name": "test recurring tests 2",
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
    response = Response(json.dumps(data,ensure_ascii = False), content_type="application/json; charset=utf-8")
    return response


#@app.route('/return_test_results', methods=['GET'])
#def return_test_results():
def return_test_results(name, result_value):
#    name = request.args.get('Lapse_eesnimi')
#    result_value = request.args.get('result_value')

    if TestResults.query.filter_by(lapse_eesnimi = name.lower(), result_value = result_value).first() is None:
      out_text = "no_results"

    else:
      data = TestResults.query.filter_by(lapse_eesnimi = name.lower(), result_value = result_value).all()
      result_dict = [u.__dict__ for u in data]
      block_name = [d.get('block_name') for d in result_dict]    
      block_name = str(block_name)

      block_name = block_name.replace('[u"', "")
      block_name = block_name.replace('", u"',', ')
      block_name = block_name.replace('"','')
      block_name = block_name.replace('[','')
      block_name = block_name.replace(']','')

      query = "SELECT group_concat(m.description, ', '), 'a' FROM tests t JOIN milestone_tests ms ON t.id_test = ms.key_test JOIN milestones m ON ms.key_milestone = m.id_milestone WHERE t.block_name IN (%s) LIMIT 1;" % (block_name)    
      rows = execute_query(query)
      out_text = str(rows[0][0].encode("utf-8"))
    return str(out_text)


@app.route('/tests_summary', methods=['GET'])
def tests_summary():

    name = request.args.get('Lapse_eesnimi')
    dob = request.args.get('Synni_kuupaev')
    date_object = datetime.strptime(dob, "%Y-%m-%d").date()
    age = date.today() - date_object
    age_months = str(int(age.days)/30)

    if TestResults.query.filter_by(lapse_eesnimi = name.lower()).first() is None:
      out_text = u"Ühtegi testi pole veel tehtud"

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
                      "block_name": "test recurring tests 2",
                      "title": "Tagasi testima"
                    }
                  ]
                }
              }
            }
          ]
        }


    else:

      data_jah = str(return_test_results(name, 'Jah'))
      data_ei = str(return_test_results(name, 'Ei'))
      data_ei_tea = str(return_test_results(name, 'Ei tea'))

      if (str(data_jah) != 'no_results' and str(data_ei) == 'no_results'):
        data = {
            "messages": [
              {
                "attachment": {
                  "type": "template",
                  "payload": {
                    "template_type": "button",
                    "text": str(name) + " on " + age_months + " kuu vanune ja ta oskab " + data_jah,
                    "buttons": [
                      {
                        "type": "show_block",
                        "block_name": "test recurring tests 2",
                        "title": "Tagasi testima"
                      }
                    ]
                  }
                }
              }
            ]
          }

      elif (str(data_jah) != 'no_results' and str(data_ei) != 'no_results'):
        data = {
            "messages": [
              {"text": str(name) + " on " + age_months + " kuu vanune ja ta oskab " + data_jah + ","},
              {
                "attachment": {
                  "type": "template",
                  "payload": {
                    "template_type": "button",
                    "text": "aga " + name + " ei oska eriti veel ise " + data_ei + ".",
                    "buttons": [
                      {
                        "type": "show_block",
                        "block_name": "test recurring tests 2",
                        "title": "Tagasi testima"
                      }
                    ]
                  }
                }
              }
            ]
          }



      else:
        data = {
            "messages": [
              {
                "attachment": {
                  "type": "template",
                  "payload": {
                    "template_type": "button",
                    "text": u"aga ta ei oska hästi veel ise " + data_ei,
                    "buttons": [
                      {
                        "type": "show_block",
                        "block_name": "test recurring tests 2",
                        "title": "Tagasi testima"
                      }
                    ]
                  }
                }
              }
            ]
          }

    response = Response(json.dumps(data,ensure_ascii = False), content_type="application/json; charset=utf-8")
    return response


'''
      if (str(data_jah) != 'no_results' and str(data_ei) == 'no_results'):
#        out_text = u"Tänan! " + name + u" on omandanud kõik " + str(data_jah) + u" peamist oskust, mida selles vanuses lapse arengu hindamisel jälgitakse."
        out_text = str(data_jah)

        button_1_block = "Default answer"
        button_1_title = u"Küsin veel"

        button_2_block = "Default answer"
        button_2_title = u"Ootan juhiseid"

        button_3_block = "Default answer"
        button_3_title = u"Sisestan ise"

      elif (str(data_jah) != 'no_results' and str(data_ei) != 'no_results'):
        out_text = u"Tänan! " + name + u" on juba omadanud " + str(data_jah) + u" lapse arengus jälgitavat oskust. " + name + u" õpib praegu veel: "+ str(data_ei) + u" oskust."

        button_1_block = "Default answer"
        button_1_title = u"Selge, aitäh!"

        button_2_block = "Default answer"
        button_2_title = u"Kuidas toetada?"

        button_3_block = "Default answer"
        button_3_title = u"Soovin meeldetuletusi."

      elif (str(data_jah) == 'no_results' and str(data_ei) != 'no_results'):
        out_text = u"Tänan! " + name + u" praegu veel õpib " + str(data_ei) + u" peamist eakohast oskust."

        button_1_block = "Default answer"
        button_1_title = u"Perearstile"

        button_2_block = "Default answer"
        button_2_title = u"Kuidas toetada?"

        button_3_block = "Default answer"
        button_3_title = u"Soovin meeldetu"

      else:
        out_text = u"Some error"

        button_1_block = "Default answer"
        button_1_title = u"Perearstile"

        button_2_block = "Default answer"
        button_2_title = u"Kuidas toetada?"

        button_3_block = "Default answer"
        button_3_title = u"Soovin meeldetu"

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
                    "block_name": button_1_block,
                    "title": button_1_title
                  },
                  {
                    "type": "show_block",
                    "block_name": button_2_block,
                    "title": button_2_title
                  },
                  {
                    "type": "show_block",
                    "block_name": button_3_block,
                    "title": button_3_title
                  }
                ]
              }
            }
          }
        ]
      }

    response = Response(json.dumps(data,ensure_ascii = False), content_type="application/json; charset=utf-8")
    return response
'''

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

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
