from flask import Flask
import joblib

app = Flask(__name__)

app.config.from_pyfile('config.cfg')

joblib_file = "./application/static/model.pkl"
ai_model = joblib.load(joblib_file)

from application import routes