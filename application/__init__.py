from flask import Flask
import joblib
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

app = Flask(__name__)

app.config.from_pyfile('config.cfg')
heroku = Heroku(app)

db = SQLAlchemy(app)

joblib_file = "./application/static/model.pkl"
ai_model = joblib.load(joblib_file)

from application import routes