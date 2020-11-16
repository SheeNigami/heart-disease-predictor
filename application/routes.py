from application import app
from flask import render_template
 
#Handles http://127.0.0.1:5000/
@app.route('/') 
@app.route('/index') 
@app.route('/home') 
def index_page(): 
    return render_template("index.html")