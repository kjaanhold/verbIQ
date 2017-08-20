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

    id = db.Column(db.Integer, db.Sequence('seq_reg_id', start=10000, increment=1), primary_key = True)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    date_created = db.Column(db.DateTime)

    def __init__(self, id, lat, lng, date_created):
    	self.id = id
    	self.lat = lat
    	self.lng = lng
        self.date_created = date_created


class TestResults(BaseModel, db.Model):
    """Model for the test_results table"""
    __tablename__ = 'test_results'

    id_test_result = db.Column(db.Integer, primary_key = True)
    key_user = db.Column(db.Integer)
    block_name = db.Column(db.String)
    lapse_eesnimi = db.Column(db.String)
    date_created = db.Column(db.DateTime)
    result_type = db.Column(db.String)
    result_value = db.Column(db.String)

    def __init__(self, id_test_result, key_user, block_name,lapse_eesnimi,date_created,result_type,result_value):
        self.id_test_result = id_test_result
        self.key_user = key_user
        self.block_name = block_name
        self.lapse_eesnimi = lapse_eesnimi
        self.date_created = date_created
        self.result_type = result_type
        self.result_value = result_value





