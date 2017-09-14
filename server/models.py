from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


class Station(BaseModel, db.Model):
    """Model for the stations table"""
    __tablename__ = 'stations'

    id = db.Column(db.Integer, primary_key = True)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    last_updated = db.Column(db.DateTime)
    def __init__(self, lat, lng, last_updated):
    	self.lat = lat
    	self.lng = lng
        self.last_updated = last_updated

class TestResults(BaseModel, db.Model):
    """Model for the test_results table"""
    __tablename__ = 'test_results'

    id_test_result = db.Column(db.Integer, primary_key = True)
    key_user = db.Column(db.String)
    block_name = db.Column(db.String)
    lapse_eesnimi = db.Column(db.String)
    date_created = db.Column(db.DateTime)
    result_type = db.Column(db.String)
    result_value = db.Column(db.String)

    def __init__(self,key_user,block_name,lapse_eesnimi,date_created,result_type,result_value):
        self.key_user = key_user
        self.block_name = block_name
        self.lapse_eesnimi = lapse_eesnimi
        self.date_created = date_created
        self.result_type = result_type
        self.result_value = result_value

    @property
    def json(self):
        return to_json(self, self.__class__)

class Test(BaseModel, db.Model):
    """Model for the test table"""
    __tablename__ = 'test'

    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.String)
    block_name = db.Column(db.String)
    description = db.Column(db.String)
    follow_up_question = db.Column(db.String)

    id_test = db.Column(db.Integer, db.ForeignKey("milestones.id_milestones_test"))
    
    def __init__(self,channel,block_name,description,follow_up_question,id_test):
        self.channel = channel
        self.block_name = block_name
        self.description = description
        self.follow_up_question = follow_up_question
        self.id_test = id_test

    @property
    def json(self):
        return to_json(self, self.__class__)

class MilestoneTests(BaseModel, db.Model):
    """Model for the test table"""
    __tablename__ = 'milestones'

    id_milestones_test = db.Column(db.Integer, primary_key = True)
    target_age = db.Column(db.Integer)
    type = db.Column(db.String)
    description = db.Column(db.String)
    key_milestone = db.Column(db.String)
    
    def __init__(self,target_age,type,description,key_milestone):
        self.target_age = target_age
        self.type = type
        self.description = description
        self.key_test = key_test
        self.key_milestone = key_milestone



class Children(BaseModel, db.Model):
    """Model for the children table"""
    __tablename__ = 'children'

    id = db.Column(db.Integer, primary_key=True)
    key_user = db.Column(db.String)
    lapse_eesnimi = db.Column(db.String)
    date_of_birth = db.Column(db.DateTime)
    gender = db.Column(db.String)
    first_updated = db.Column(db.DateTime)
    last_updated = db.Column(db.DateTime)

    def __init__(self,key_user,lapse_eesnimi,date_of_birth,gender,first_updated,last_updated):
        self.key_user = key_user
        self.lapse_eesnimi = lapse_eesnimi
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.first_updated = first_updated
        self.last_updated = last_updated





