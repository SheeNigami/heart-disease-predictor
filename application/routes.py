from flask import render_template
from application.forms import PredictionForm
 
#Handles http://127.0.0.1:5000/
@app.route('/') 
@app.route('/index') 
@app.route('/home') 
def index_page(): 
    form1 = PredictionForm()
    return render_template("index.html", form=form1, title="Enter Parameters")
