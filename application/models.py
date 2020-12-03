from application import db
import datetime as dt
from sqlalchemy.orm import validates

class Entry(db.Model): 
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    age = db.Column(db.Integer)
    height = db.Column(db.Integer)
    weight = db.Column(db.Float)
    gender = db.Column(db.Integer)
    s_blood_pressure = db.Column(db.Integer)
    d_blood_pressure = db.Column(db.Integer)
    cholesterol = db.Column(db.Integer)
    glucose = db.Column(db.Integer)
    smoking = db.Column(db.Integer)
    alcohol = db.Column(db.Integer)
    physical = db.Column(db.Integer)

    prediction = db.Column(db.Integer)
    predicted_on = db.Column(db.DateTime, nullable=False)

    @validates('s_blood_pressure')
    def validate_sbp(self, key, s_blood_pressure): 
        if s_blood_pressure <= 0:
            raise AssertionError('Value must be positive')
        return s_blood_pressure

    @validates('d_blood_pressure')
    def validate_sbp(self, key, d_blood_pressure): 
        if d_blood_pressure <= 0:
            raise AssertionError('Value must be positive')
        return d_blood_pressure
    