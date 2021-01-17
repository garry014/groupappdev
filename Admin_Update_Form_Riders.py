from wtforms import Form, StringField, SelectField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import Regexp, InputRequired, Length


class UpdateAdmin(Form):
    firstname = StringField('Firstname', [validators.Length(min=1, max=100), validators.DataRequired()])
    lastname = StringField('Lastname', [validators.Length(min=1, max=100), validators.DataRequired()])
    user_name = StringField('Username (minimum 6 characters)', [validators.Length(min=6, max=30), validators.DataRequired()])
    email = EmailField('Email',  validators=[InputRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
    phone_number = StringField('Phone Number', [Length(8), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'),('N', 'Rather not say')], default='')
    transport = SelectField('Transport', [validators.DataRequired()], choices=[('', 'Select'), ('Van/Car', 'Van/Car'), ('Motorcycle', 'Motorcycle'), ('Bicycle', 'Bicycle'), ('On Foot', 'On Foot')], default='')
    license_number = StringField('License No Eg. 123456789A', [validators.DataRequired(), Regexp('[0-9]{9}[A-Z]{1}')])
