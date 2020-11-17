from application import app
from flask import render_template, request, flash
from application.forms import PredictionForm
 
#Handles http://127.0.0.1:5000/
@app.route('/') 
@app.route('/index') 
@app.route('/home') 
def index_page(): 
    form1 = PredictionForm()
    return render_template("index.html", form=form1, title="Enter Parameters")

@app.route("/predict", methods=['GET','POST'])
def predict():
    form = PredictionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            age = form.age.data
            height = form.height.data
            weight = form.weight.data
            gender = form.gender.data
            print(gender)
            s_blood_pressure = form.s_blood_pressure.data
            d_blood_pressure = form.d_blood_pressure.data
            cholesterol = form.cholesterol.data
            glucose = form.glucose.data
            smoking = form.smoking.data
            alcohol = form.alcohol.data
            physical = form.physical.data
            flash(f"Prediction: ","success")
        else:
            flash("Error, cannot proceed with prediction","danger")
    return render_template("index.html", title="Enter Iris Parameters", form=form, index=True )