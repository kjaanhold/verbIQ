# -*- coding: utf-8 -*-
import csv
import sqlite3
import json
import math
# import scipy

from flask import Flask, request, g, jsonify, Response
from datetime import datetime, date
from models import db, Station, TestResults, Test, MilestoneTests, Children
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
      result_cdf_value = request.form['test_result_cdf']
      result_cdf_value = float(result_cdf_value)

      if (result_value == "Jah" and result_cdf_value < 0.5):
        result_cdf_value = float(1) - result_cdf_value
      elif (result_value == "Ei" and result_cdf_value > 0.5):
        result_cdf_value = float(1) - result_cdf_value
      elif (result_value == "Ei tea"):
        result_cdf_value = -1
      else:
        result_cdf_value = 0.5

      new_data = TestResults(key_user=str(key_user), block_name=str("'"+block_name+"'"), lapse_eesnimi=str(lapse_eesnimi.encode('utf8')), date_created=str(date_created), result_type=str(result_type), result_value=str(result_value), result_cdf_value = float(result_cdf_value))
      db.session.add(new_data)
      db.session.commit()


      child = Children.query.filter_by(key_user = key_user, lapse_eesnimi = lapse_eesnimi).first()
      child.last_updated = datetime.utcnow()
      db.session.commit()

      data = {
        "redirect_to_blocks": ["test recurring tests 2"]
      }
      return jsonify(data)

    if request.method == "GET":
#      out = TestResults.query.order_by(TestResults.date_created.desc()).first()
      n1 = request.args.get('messenger user id')
      n2 = request.args.get('last_visited_block_id')
      n3 = request.args.get('Lapse_eesnimi')
      n4 = request.args.get('test_result')

      data = {'messages':[{"text": "id_test_result: " + " / " + str(n1) + " / "  + ", " + str(n2) + " / "  + ", " + str(n3) + " / " + ", " + str(n4)}]}
      return jsonify(data)


@app.route('/has_children', methods = ['GET'])
def has_children():
    key_user = request.args.get('messenger user id')

    if Children.query.filter_by(key_user = key_user).count() == 0:
      data = {
        'messages':[{"text": u"Tore! Palun sisesta oma lapse andmed."}], 
        "redirect_to_blocks": ["create_child"]
      }

      return jsonify(data)

    else: 
      data = {"redirect_to_blocks": ["returning_parents"]}
      return jsonify(data)

@app.route('/has_enough_children', methods = ['GET'])
def has_enough_children():
    key_user = request.args.get('messenger user id')

    if Children.query.filter_by(key_user = key_user).count() > 2:
      data = {
          'messages':[{"text": u"Üle kolme lapse ei saa sisestada."}], 
          "redirect_to_blocks": ["returning_parents"]
        }
      return jsonify(data)

    else: 
      data = {'messages':[{"text": "Tore! Palun sisesta oma lapse andmed."}]}
      return jsonify(data)

## work in progress
@app.route('/child_selection', methods = ['GET'])
def child_selection():
    key_user = request.args.get('messenger user id')

    if Children.query.filter_by(key_user = key_user).count() == 0:
      data = {
        "messages": [
          {
            "attachment": {
              "type": "template",
              "payload": {
                "template_type": "button",
                "text": u"Sul pole vel ühtegi last sisestatud.",
                "buttons": [
                  {
                    "block_names": ["create_child"],
                    "type": "show_block",
                    "title": "Lisa uus laps"
                  }

                ]
              }
            }
          }
        ]
      }      


    elif Children.query.filter_by(key_user = key_user).count() == 1:
      data = Children.query.filter_by(key_user = key_user).all()
      result_dict = [u.__dict__ for u in data]

      child_name = [d.get('lapse_eesnimi') for d in result_dict]    
      child_name_1 = child_name[0]

      date_of_birth = [d.get('date_of_birth') for d in result_dict]    
      date_of_birth_1 = date_of_birth[0]

      data = {
        "messages": [
          {
            "attachment": {
              "type": "template",
              "payload": {
                "template_type": "button",
                "text": u"Kelle kohta sooovid infot sisestada?",
                "buttons": [
                  {
                    "set_attributes": 
                      {
                        "Lapse_eesnimi": str(child_name_1),
                        "Synni_kuupaev": str(date_of_birth_1)
                      },
                    "block_names": ["returning_parents"],
                    "type": "show_block",
                    "title": str(child_name_1)
                  },
                  {
                    "block_names": ["create_child"],
                    "type": "show_block",
                    "title": "Lisa uus laps"
                  }
                ]
              }
            }
          }
        ]
      }      


    elif Children.query.filter_by(key_user = key_user).count() == 2:      
      data = Children.query.filter_by(key_user = key_user).all()
      result_dict = [u.__dict__ for u in data]

      child_name = [d.get('lapse_eesnimi') for d in result_dict]    
      child_name_1 = child_name[0]
      child_name_2 = child_name[1]

      date_of_birth = [d.get('date_of_birth') for d in result_dict]    
      date_of_birth_1 = date_of_birth[0]
      date_of_birth_2 = date_of_birth[1]


      data = {
        "messages": [
          {
            "attachment": {
              "type": "template",
              "payload": {
                "template_type": "button",
                "text": u"Kelle kohta sooovid infot sisestada?",
                "buttons": [
                  {
                    "set_attributes": 
                      {
                        "Lapse_eesnimi": str(child_name_1),
                        "Synni_kuupaev": str(date_of_birth_1)
                      },
                    "block_names": ["returning_parents"],
                    "type": "show_block",
                    "title": str(child_name_1)
                  },
                  {
                    "set_attributes": 
                      {
                        "Lapse_eesnimi": str(child_name_2),
                        "Synni_kuupaev": str(date_of_birth_2)
                      },
                    "block_names": ["returning_parents"],
                    "type": "show_block",
                    "title": str(child_name_2)
                  },
                  {
                    "block_names": ["create_child"],
                    "type": "show_block",
                    "title": "Lisa uus laps"
                  }

                ]
              }
            }
          }
        ]
      }      

    elif Children.query.filter_by(key_user = key_user).count() == 3:      
      data = Children.query.filter_by(key_user = key_user).all()
      result_dict = [u.__dict__ for u in data]

      child_name = [d.get('lapse_eesnimi') for d in result_dict]    
      child_name_1 = child_name[0]
      child_name_2 = child_name[1]
      child_name_3 = child_name[2]

      date_of_birth = [d.get('date_of_birth') for d in result_dict]    
      date_of_birth_1 = date_of_birth[0]
      date_of_birth_2 = date_of_birth[1]
      date_of_birth_3 = date_of_birth[2]

      data = {
        "messages": [
          {
            "attachment": {
              "type": "template",
              "payload": {
                "template_type": "button",
                "text": u"Kelle kohta sooovid infot sisestada?",
                "buttons": [
                  {
                    "set_attributes": 
                      {
                        "Lapse_eesnimi": str(child_name_1),
                        "Synni_kuupaev": str(date_of_birth_1)
                      },
                    "block_names": ["returning_parents"],
                    "type": "show_block",
                    "title": str(child_name_1)
                  },
                  {
                    "set_attributes": 
                      {
                        "Lapse_eesnimi": str(child_name_2),
                        "Synni_kuupaev": str(date_of_birth_2)
                      },
                    "block_names": ["returning_parents"],
                    "type": "show_block",
                    "title": str(child_name_2)
                  },
                  {
                    "set_attributes": 
                      {
                        "Lapse_eesnimi": str(child_name_3),
                        "Synni_kuupaev": str(date_of_birth_3)
                      },
                    "block_names": ["returning_parents"],
                    "type": "show_block",
                    "title": str(child_name_3)
                  }
                ]
              }
            }
          }
        ]
      }      

    else: 

      data = {
        "redirect_to_blocks": ["returning_parents"]
      }


    response = Response(json.dumps(data,ensure_ascii = False), content_type="application/json; charset=utf-8")
    return response


@app.route('/store_children', methods = ['GET','POST'])
def store_children():
    if request.method == "POST":
      key_user = request.form['messenger user id']
      lapse_eesnimi = request.form['Lapse_eesnimi']
      date_of_birth = request.form['Synni_kuupaev']
      gender = request.form['Lapse_sugu']
      first_updated = datetime.utcnow()
      last_updated = datetime.utcnow()

      new_data = Children(key_user=str(key_user), lapse_eesnimi=str(lapse_eesnimi.encode('utf8')), date_of_birth=str(date_of_birth), gender=str(gender.encode('utf8')), first_updated=str(first_updated), last_updated=str(last_updated))
      db.session.add(new_data)
      db.session.commit()
      data = {"redirect_to_blocks": ["returning_parents"]}
      return jsonify(data)

    if request.method == "GET":
      data = {'messages':[{"text": "error!"}]}
      return jsonify(data)

'''
## update children table
      else: 
        child = Children.query.filter_by(key_user = key_user, lapse_eesnimi = lapse_eesnimi).first()
        child.last_updated = datetime.utcnow()
        db.session.commit()
        data = {'messages':[{"text": "..."}]}
        return jsonify(data)
'''


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
def next_test_selection(dob,name,last_block):
#def next_test_selection():
#    dob = request.args.get('Synni_kuupaev')
#    name = request.args.get('Lapse_eesnimi')

    date_object = datetime.strptime(dob, "%Y-%m-%d").date()
    age = date.today() - date_object
    age_months = str(int(age.days)/30)

      # this kid hasn't done any tests yet
    if TestResults.query.filter_by(lapse_eesnimi = name).first() is None:

      query = "SELECT t.description, t.block_name, m.target_age FROM tests t JOIN milestone_tests ms ON t.id_test = ms.key_test JOIN milestones m ON ms.key_milestone = m.id_milestone WHERE m.target_age BETWEEN (2*%s)/3 AND (4*%s)/3 ORDER BY RANDOM() LIMIT 1;" % (age_months, age_months)
      rows = execute_query(query)

      question = str(rows[0][0].encode("utf-8"))
      block_name = str(rows[0][1].encode("utf-8"))
      target_age = str(rows[0][2])

    elif (last_block == "update_previous_tests"):
      # this kid has done at least one test
      data = TestResults.query.filter_by(lapse_eesnimi = name, result_value = 'Jah').all()
      result_dict = [u.__dict__ for u in data]
      block_name = [d.get('block_name') for d in result_dict]
      block_name = str(block_name)
      block_name = block_name.replace('u"','')
      block_name = block_name.replace('"','')
#      block_name = block_name.replace("u'","'")
      block_name = block_name.replace('[','')
      block_name = block_name.replace(']','')
 
      query = "SELECT t.description, t.block_name, m.target_age FROM tests t JOIN milestone_tests ms ON t.id_test = ms.key_test JOIN milestones m ON ms.key_milestone = m.id_milestone WHERE ( m.target_age BETWEEN (2*%s)/3 AND (4*%s)/3 ) AND t.block_name NOT IN (%s) ORDER BY RANDOM() LIMIT 1;" % (age_months, age_months, block_name)    

      rows = execute_query(query)

      if str(rows) == '[]':
        question  = 'done'
        block_name = 'test_summary'
        target_age = str("0")

      else:
        question = str(rows[0][0].encode("utf-8"))
        block_name = str(rows[0][1].encode("utf-8"))
        target_age = str(rows[0][2])

    else:
      # this kid has done at least one test
      data = TestResults.query.filter_by(lapse_eesnimi = name).all()
      result_dict = [u.__dict__ for u in data]
      block_name = [d.get('block_name') for d in result_dict]
      block_name = str(block_name)
      block_name = block_name.replace('u"','')
      block_name = block_name.replace('"','')
#      block_name = block_name.replace("u'","'")
      block_name = block_name.replace('[','')
      block_name = block_name.replace(']','')
 
      query = "SELECT t.description, t.block_name, m.target_age FROM tests t JOIN milestone_tests ms ON t.id_test = ms.key_test JOIN milestones m ON ms.key_milestone = m.id_milestone WHERE ( m.target_age BETWEEN (2*%s)/3 AND (4*%s)/3 ) AND t.block_name NOT IN (%s) ORDER BY RANDOM() LIMIT 1;" % (age_months, age_months, block_name)    

      rows = execute_query(query)

      if str(rows) == '[]':
        question  = 'done'
        block_name = 'test_summary'
        target_age = str("0")

      else:
        question = str(rows[0][0].encode("utf-8"))
        block_name = str(rows[0][1].encode("utf-8"))
        target_age = str(rows[0][2])

    return str(question) + '///' + str(block_name) + '///' + str(target_age)





@app.route('/run_test', methods=['GET'])
def run_test():
    dob = request.args.get('Synni_kuupaev')
    name = request.args.get('Lapse_eesnimi')
    last_block =  request.args.get('last visited block name') 

    selected_test = next_test_selection(dob = dob, name = name, last_block = last_block)

    question = str(selected_test.split("///")[0])
    block_name = str(selected_test.split("///")[1])

    if question == "done":
      data = {"redirect_to_blocks": ["test_summary"]}

    else:
      date_object = datetime.strptime(dob, "%Y-%m-%d").date()
      age = date.today() - date_object
      age_months = float(age.days)/30

      target_age = float(selected_test.split("///")[2])
      variance = float("1")
      cdf = lognorm(age_months, target_age, variance)

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
                      "test_result": "Jah",
                      "test_result_cdf": str(cdf)
                    },
                    "type": "show_block",
                    "block_name": "test recurring tests 3",
                    "title": u"Jah"
                  },
                  {
                    "set_attributes": 
                    {
                      "test_result": "Ei tea",
                      "test_result_cdf": str(cdf)                      
                    },
                    "type": "show_block",
                    "block_name": "test recurring tests 3",
                    "title": u"Ei tea"
                  },                
                  {
                    "set_attributes": 
                    {
                      "test_result": "Ei",
                      "test_result_cdf": str(cdf)                      
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





#@app.route('/lognorm', methods=['GET'])
#def lognorm():
def lognorm(x, mean, var):
#  x = float(request.args.get('x'))  
#  mean = float(request.args.get('mean'))  
#  var = float(request.args.get('var'))  

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
                  "block_name": "insert_child",
                  "title": u"Õige, edasi!"
                },
                {
                  "type": "show_block",
                  "block_name": "create_child",
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

    if TestResults.query.filter_by(lapse_eesnimi = name, result_value = result_value).first() is None:
      out_text = "no_results"

    else:
      data = TestResults.query.filter_by(lapse_eesnimi = name, result_value = result_value).all()
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

def return_test_score(name):

    if TestResults.query.filter_by(lapse_eesnimi = name).first() is None:
      out_text = "0"
    else:
      data = TestResults.query.filter_by(lapse_eesnimi = name).all()
      result_dict = [u.__dict__ for u in data]
      result_cdf_value = [d.get('result_cdf_value') for d in result_dict if d.get('result_cdf_value') >= 0]    
      result_cdf_value = str(round(sum(result_cdf_value)*2*100/len(result_cdf_value)))

      bottom_skills_data = TestResults.query.filter_by(lapse_eesnimi = name, result_value = "Ei").order_by(TestResults.result_cdf_value.asc()).limit(3)
      bottom_result_dict = [u.__dict__ for u in bottom_skills_data]
      bottom_block_name = [d.get('block_name') for d in bottom_result_dict]    
      bottom_block_name = str(bottom_block_name)

      bottom_block_name = bottom_block_name.replace('[u"', "")
      bottom_block_name = bottom_block_name.replace('", u"',', ')
      bottom_block_name = bottom_block_name.replace('"','')
      bottom_block_name = bottom_block_name.replace('[','')
      bottom_block_name = bottom_block_name.replace(']','')

      query = "SELECT group_concat(m.description, ', '), 'a' FROM tests t JOIN milestone_tests ms ON t.id_test = ms.key_test JOIN milestones m ON ms.key_milestone = m.id_milestone WHERE t.block_name IN (%s) LIMIT 1;" % (bottom_block_name)    
      rows = execute_query(query)

      bottom_block_descriptions = str(rows[0][0].encode("utf-8"))

      out_text = str(result_cdf_value) + "///" + str(bottom_block_descriptions) + "///" + str(bottom_block_name) # + ", bottom blocks:" + str(bottom_block_name)
    return str(out_text)


@app.route('/tests_summary', methods=['GET'])
def tests_summary():

    name = request.args.get('Lapse_eesnimi')
    dob = request.args.get('Synni_kuupaev')
    date_object = datetime.strptime(dob, "%Y-%m-%d").date()
    age = date.today() - date_object
    age_months = str(int(age.days)/30)


    if TestResults.query.filter_by(lapse_eesnimi = name).first() is None:
      out_text = name + u" pole veel ühtegi testi teinud."

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
                      "block_name": "returning_parents",
                      "title": "Tagasi"
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
      returned_test_score = str(return_test_score(name))
      score = str(returned_test_score.split("///")[0]) 
      weaknesses = str(returned_test_score.split("///")[1]) 
      #str(returned_test_score.split("///")[0])
      #weaknesses = str(returned_test_score.split("///")[1])

      if (str(data_jah) != 'no_results' and str(data_ei) == 'no_results'):
        data = {
            "messages": [
#              {"text": str(name) + " on " + age_months + " kuu vanune ja ta oskab " + data_jah + "."},
              {
                "attachment": {
                  "type": "template",
                  "payload": {
                    "template_type": "button",
                    "text":  str(name) + " skoor on " + score + " (keskmise lapse skoor selles vanuses on 100).",
                    "buttons": [
                      {
                        "type": "show_block",
                        "block_name": "returning_parents",
                        "title": "Tagasi"
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
#              {"text": str(name) + " on " + age_months + " kuu vanune ja ta oskab " + data_jah + ","},
#              {"text": "aga " + str(name) + " ei oska eriti veel ise " + data_ei + "."},
              {
                "attachment": {
                  "type": "template",
                  "payload": {
                    "template_type": "button",
                    "text":  str(name) + " skoor on " + score + " (keskmise lapse skoor selles vanuses on 100). Taseme parandamiseks peaks ta esmalt suutma " + weaknesses,
                    "buttons": [
                      {
                        "type": "show_block",
                        "block_name": "test_summary_hidden",
                        "title": "Treenima"
                      },
                      {
                        "type": "show_block",
                        "block_name": "returning_parents",
                        "title": "Tagasi"
                      }
                    ]
                  }
                }
              }
            ]
          }

      elif (str(data_jah) == 'no_results' and str(data_ei) != 'no_results'):
        data = {
            "messages": [
#              {"text": str(name) + " on " + age_months + " kuu vanune ja ei oska veel " + data_ei + "."},
              {
                "attachment": {
                  "type": "template",
                  "payload": {
                    "template_type": "button",
                    "text":  str(name) + " skoor on " + score + " (keskmise lapse skoor selles vanuses on 100). Taseme parandamiseks peaks ta esmalt suutma "+ weaknesses,
                    "buttons": [
                      {
                        "type": "show_block",
                        "block_name": "test_summary_hidden",
                        "title": "Treenima"
                      },
                      {
                        "type": "show_block",
                        "block_name": "returning_parents",
                        "title": "Tagasi"
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
                    "text": "viga",
                    "buttons": [
                      {
                        "type": "show_block",
                        "block_name": "returning_parents",
                        "title": "Tagasi"
                      }
                    ]
                  }
                }
              }
            ]
          }

    response = Response(json.dumps(data,ensure_ascii = False), content_type="application/json; charset=utf-8")
    return response

@app.route('/propose_exercise/', methods=['GET'])
def propose_exercise():
    name = request.args.get('Lapse_eesnimi')
    returned_test_score = str(return_test_score(name))
    bottom_block_name = str(returned_test_score.split("///")[2]) 
    query = "SELECT m.description, e.description_est FROM tests t  JOIN milestone_tests ms ON t.id_test = ms.key_test JOIN milestones m ON ms.key_milestone = m.id_milestone JOIN milestone_tests ms ON t.id_test = ms.key_test JOIN milestones_exercises me ON ms.key_milestone = me.key_milestone JOIN exercises e ON me.key_exercise = e.id_exercise WHERE t.block_name IN (%s) LIMIT 3;" % (bottom_block_name)    
    rows = execute_query(query)
    out_text = str(rows[1][1].encode("utf-8"))
    return str(out_text)




#    return str(query)



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