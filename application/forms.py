from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, SelectField
from wtforms.validators import Length, InputRequired, ValidationError, NumberRange
 
class PredictionForm(FlaskForm):
    age = IntegerField("Age", 
            validators=[InputRequired(), NumberRange(0,150)])
    height = IntegerField("Height",
            validators=[InputRequired(), NumberRange(50,300)])
    weight = FloatField("Weight",
            validators=[InputRequired(), NumberRange(5,500)])
    gender = SelectField("Gender", choices=[('Male', ''), ('Female', '')]
            default=('Male', '') )
    s_blood_pressure = IntegerField("Systolic blood pressure",
            validators=[InputRequired()])
    d_blood_pressure = IntegerField("Diastolic blood pressure", 
            validators=[InputRequired()])
    cholesterol = SelectField('Cholesterol', 
            default=('1', 'Normal'), choices=[('1', 'Normal'), ('2', 'Above Normal'), ('3', 'Well Above Normal')])
    glucose = SelectField('Glucose', 
            default=('1', 'Normal'), choices=[('1', 'Normal'), ('2', 'Above Normal'), ('3', 'Well Above Normal')])
    smoking = SelectField('Smoking', 
            default=('0', "No"), choices=[('0', 'No'), ('1', 'Yes')])
    alcohol = SelectField('Alcohol Intake', 
            default=('0', "No"), choices=[('0', "No"), ('1', 'Yes')])
    physical = SelectField('Physical Activity', 
            default=('0', "No"), choices=[('0', "No"), ('1', 'Yes')])
    submit = SubmitField("Predict")