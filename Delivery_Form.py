from wtforms import Form, StringField, SelectField, validators
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import InputRequired, Length


class Deliver_Options(Form):
    firstname = StringField('Firstname', [validators.Length(min=1, max=100), validators.DataRequired()])
    lastname = StringField('Lastname', [validators.Length(min=1, max=100), validators.DataRequired()])
    address1 = StringField("Address Line 1", [validators.DataRequired()])
    address2 = StringField("Address Line 2", [validators.DataRequired()])
    city = StringField("City", [validators.DataRequired()])
    postal_code = StringField('Postal Code', [Length(6), validators.DataRequired()])
    email = EmailField('Email',  validators=[InputRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
    phone_number = StringField('Phone Number', [Length(8), validators.DataRequired()])
    order_notes = StringField('Additional information')
    delivery_options = SelectField('Delivery Options', [validators.DataRequired()], choices=[('', 'Select'), ('Self Collection', 'Self Collection'), ('Home Delivery', 'Home Delivery')], default='')
    delivery_time = SelectField('Preferred Timing', [validators.DataRequired()], choices=[('', 'select'), ('9:00am', '9:00am'), ('12:00pm', '12:00pm'), ('3:00pm', '3:00pm'), ('6:00pm', '6:00pm'), ('9:00pm', '9:00pm')])
    delivery_date = DateField('Preferred Date', validators=[validators.DataRequired()], format='%Y-%m-%d')

