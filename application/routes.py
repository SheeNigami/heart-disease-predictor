from application import app, ai_model, db
from flask import render_template, request, flash, json, jsonify
from application.forms import PredictionForm
from application.models import Entry
from datetime import datetime

display_result = ['Cardiovascular Disease Absent', 'Cardiovascular Disease Present']
db.create_all()
 
#Handles http://127.0.0.1:5000/
@app.route('/') 
@app.route('/index') 
@app.route('/home') 
def index_page(): 
    form1 = PredictionForm()
    return render_template("index.html", form=form1, 
                           title="Enter Parameters", 
                           entries = get_entries()) 

@app.route("/predict", methods=['GET','POST'])
def predict():
    form = PredictionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            age = form.age.data
            height = form.height.data
            weight = form.weight.data
            gender = form.gender.data
            s_blood_pressure = form.s_blood_pressure.data
            d_blood_pressure = form.d_blood_pressure.data
            cholesterol = form.cholesterol.data
            glucose = form.glucose.data
            smoking = form.smoking.data
            alcohol = form.alcohol.data
            physical = form.physical.data

            bmi = weight / ((height/100) ** 2)
            avg_bp = (s_blood_pressure + d_blood_pressure) / 2

            X = [[age, gender, height, weight, s_blood_pressure, d_blood_pressure, cholesterol, glucose, smoking, alcohol, physical, bmi, avg_bp]]
            result = ai_model.predict(X)
            new_entry = Entry( age=age, gender=gender, height=height, weight=weight, s_blood_pressure=s_blood_pressure, d_blood_pressure=d_blood_pressure, 
                               cholesterol=cholesterol, glucose=glucose, smoking=smoking, alcohol=alcohol, physical=physical, prediction=int(result[0]), predicted_on=datetime.utcnow())
            add_entry(new_entry)
            flash(f"Prediction: {display_result[result[0]]}", "Success")
        else:
            flash("Error, cannot proceed with prediction","danger")
    return render_template("index.html", title="Enter Parameters", form=form, index=True, entries=get_entries())


@app.route('/remove', methods=['POST'])
def remove():
    form = PredictionForm()
    req = request.form
    id = req["id"]
    remove_entry(id)
    return render_template("index.html", title="Enter Parameters", form=form,
                           entries=get_entries(), index=True)


@app.route("/api/delete/<id>", methods=['GET'])
def api_delete(id): 
    entry = remove_entry(int(id))
    return jsonify({'result': 'ok'})


@app.route("/api/add", methods=['POST'])
def api_add():
    data = request.get_json()

    age = data['age']
    height = data['height']
    weight = data['weight']
    gender = data['gender']
    s_blood_pressure = data['s_blood_pressure']
    d_blood_pressure = data['d_blood_pressure']
    cholesterol = data['cholesterol']
    glucose = data['glucose']
    smoking = data['smoking']
    alcohol = data['alcohol']
    physical = data['physical']
    prediction = data['prediction']

    new_entry = Entry( age=age, gender=gender, height=height, weight=weight, s_blood_pressure=s_blood_pressure, d_blood_pressure=d_blood_pressure, 
                        cholesterol=cholesterol, glucose=glucose, smoking=smoking, alcohol=alcohol, physical=physical, prediction=prediction, predicted_on=datetime.utcnow())

    result = add_entry(new_entry)
    return jsonify({'id': result})


def add_entry(new_entry): 
    try:
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.id
    except Exception as error:
        print(error)
        db.session.rollback()
        flash(error, 'danger')


def get_entries(): 
    try:
        entries = Entry.query.all()
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")
        return 0


def remove_entry(id): 
    try:
        entry = Entry.query.get(id)
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")

    