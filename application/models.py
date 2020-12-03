from application import db
import datetime as dt
from sqlalchemy.orm import validates
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