from application import db
import datetime as dt

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