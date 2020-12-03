from flask import Flask
import joblib
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from flask_login import LoginManager
import os

app = Flask(__name__)

if "TESTING" in os.environ:
    app.config.from_envvar('TESTING')
    print("Using config for TESTING")
elif "DEVELOPMENT" in os.environ:
    app.config.from_envvar('DEVELOPMENT')
    print("Using config for DEVELOPMENT")
else:
    app.config.from_pyfile('config_dply.cfg')
    print("Using config for deployment")

heroku = Heroku(app)

db = SQLAlchemy(app)
login_manager = LoginManager(app)


joblib_file = "./application/static/model.pkl"
ai_model = joblib.load(joblib_file)

from application import routes, auth
app.register_blueprint(routes.main_bp)
app.register_blueprint(auth.auth_bp)