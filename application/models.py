from application import db
import datetime as dt
from sqlalchemy.orm import validates
from sqlalchemy import ForeignKey
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

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
    predicted_username = db.Column(db.String, ForeignKey('users.username'))
    predicted_on = db.Column(db.DateTime, nullable=False)

    # Check label encoded variables
    @validates('gender')
    def validate_gender(self, key, gender):
        if not (gender == 1 or gender == 2):
            raise AssertionError('Value must be 1 or 2 (female or male)')
        return gender

    @validates('cholesterol')
    def validate_cholesterol(self, key, cholesterol):
        if not (cholesterol == 1 or cholesterol == 2 or cholesterol == 3):
            raise AssertionError('Value must be 1/2/3')            
        return cholesterol

    @validates('glucose')
    def validate_glucose(self, key, glucose):
        if not (glucose == 1 or glucose == 2 or glucose == 3):
            raise AssertionError('Value must be 1/2/3')
        return glucose

    @validates('smoking')
    def validate_smoking(self, key, smoking):
        if not (smoking == 0 or smoking == 1):
            raise AssertionError("Value must be 0 or 1 (smoke or don't smoke)")
        return smoking
    
    @validates('alcohol')
    def validates_alcohol(self, key, alcohol):
        if not (alcohol == 0 or alcohol == 1):
            raise AssertionError("Value must be 0 or 1 (drink alcohol or not)")
        return alcohol

    @validates('physical')
    def validates_physical(self, key , physical): 
        if not (physical == 0 or physical == 1):
            raise AssertionError("Value must be 0 or 1 (exercise or not)")
        return physical

    @validates('prediction')
    def validates_prediction(self, key , prediction): 
        if not (prediction == 0 or prediction == 1):
            raise AssertionError("Value must be 0 or 1 (heart disease absent/present)")
        return prediction


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), primary_key=False, nullable=False, unique=True)
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)

    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)

    def set_password(self, password): 
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password): 
        return check_password_hash(self.password, password)

    def __repr__(self): 
        return '<User {}>'.format(self.username)