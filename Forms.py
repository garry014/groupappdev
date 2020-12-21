from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields.html5 import DateField
from datetime import date

class CreateAd(Form):
    startdate = DateField('Start Date:*', validators=[validators.DataRequired()]) #format='%Y-%m-%d'
    enddate = DateField('End Date:*', validators=[validators.DataRequired()])
