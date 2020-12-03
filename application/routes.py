from application import app, ai_model, db
from flask import render_template, request, flash, json, jsonify, Blueprint, url_for, redirect
from flask_login import current_user, login_required, logout_user
from application.forms import PredictionForm
from application.models import Entry
from datetime import datetime

display_result = ['Cardiovascular Disease Absent', 'Cardiovascular Disease Present']
db.create_all()
main_bp = Blueprint('main_bp', __name__, template_folder='templates', static_folder='static')
 
#Handles http://127.0.0.1:5000/
@main_bp.route('/') 
@main_bp.route('/index') 
@main_bp.route('/home') 
@login_required
def index_page(): 
    form1 = PredictionForm()
    return render_template("index.html", form=form1, 
                           title="Enter Parameters", 
                           entries = get_entries()) 

@main_bp.route("/predict", methods=['GET','POST'])
@login_required
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
            probability = round(ai_model.predict_proba(X)[0][int(result[0])] * 100, 2)
            new_entry = Entry( age=age, gender=gender, height=height, weight=weight, s_blood_pressure=s_blood_pressure, d_blood_pressure=d_blood_pressure, cholesterol=cholesterol, 
                               glucose=glucose, smoking=smoking, alcohol=alcohol, physical=physical, prediction=int(result[0]), predicted_on=datetime.utcnow(), predicted_username=current_user.username)
            add_entry(new_entry)
            if result[0] == 0:
                flash(f"Prediction: {display_result[result[0]]}, Probability: {probability}%", "success")
            else:
                flash(f"Prediction: {display_result[result[0]]}, Probability: {probability}%", "danger")
        else:
            flash("Error, cannot proceed with prediction", "danger")
    return render_template("index.html", title="Enter Parameters", form=form, index=True, entries=get_entries())


@main_bp.route('/remove', methods=['POST'])
@login_required
def remove():
    form = PredictionForm()
    req = request.form
    id = req["id"]
    remove_entry(id)
    return render_template("index.html", title="Enter Parameters", form=form,
                           entries=get_entries(), index=True)


@main_bp.route("/api/delete/<id>", methods=['GET'])
@login_required
def api_delete(id): 
    entry = remove_entry(int(id))
    return jsonify({'result': 'ok'})


@main_bp.route("/api/add", methods=['POST'])
@login_required
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
    predicted_username = data['predicted_username']

    new_entry = Entry( age=age, gender=gender, height=height, weight=weight, s_blood_pressure=s_blood_pressure, d_blood_pressure=d_blood_pressure, cholesterol=cholesterol, 
                       glucose=glucose, smoking=smoking, alcohol=alcohol, physical=physical, prediction=prediction, predicted_on=datetime.utcnow(), predicted_username=predicted_username)

    result = add_entry(new_entry)
    return jsonify({'id': result})


@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))


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
    gender_lookup = {1: 'Woman', 2: 'Man'}
    cholesterol_lookup = {1:'Normal', 2:'Above Normal', 3:'Well Above Normal'}
    glucose_lookup = {1:'Normal', 2:'Above Normal', 3:'Well Above Normal'}
    smoking_lookup = {0:'No', 1:'Yes'}
    alcohol_lookup = {0:'No', 1:'Yes'}
    physical_lookup = {0:'No', 1:'Yes'}
    prediction_lookup = {0: 'Absent', 1: 'Present'}
    try:
        entries = Entry.query.filter_by(predicted_username=current_user.username).all()
        for i in range(len(entries)): 
            entries[i].gender = gender_lookup[entries[i].gender]
            entries[i].cholesterol = cholesterol_lookup[entries[i].cholesterol]
            entries[i].glucose = glucose_lookup[entries[i].glucose]
            entries[i].smoking = smoking_lookup[entries[i].smoking]
            entries[i].alcohol = alcohol_lookup[entries[i].alcohol]
            entries[i].physical = physical_lookup[entries[i].physical]
            entries[i].prediction = prediction_lookup[entries[i].prediction]
            
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")
        return 0


def remove_entry(id): 
    try:
        entry = Entry.query.get(id)
        if entry.predicted_username == current_user.username:
            db.session.delete(entry)
            db.session.commit()
        else:
            db.session.rollback()
            flash("You are not looged in to the correct user", "danger")
    except Exception as error:
        db.session.rollback()
        flash(error, "danger")

    