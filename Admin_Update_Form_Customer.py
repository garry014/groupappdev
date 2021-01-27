from wtforms import Form, StringField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length


class Customer_AdminUpdate(Form):
    firstname = StringField('Firstname', [validators.Length(min=1, max=100), validators.DataRequired()])
    lastname = StringField('Lastname', [validators.Length(min=1, max=100), validators.DataRequired()])
    user_name = StringField('Username (minimum 6 characters)', [validators.Length(min=6, max=30), validators.DataRequired()])
    address1 = StringField("Address Line 1", [validators.DataRequired()])
    address2 = StringField("Address Line 2", [validators.DataRequired()])
    city = StringField("City", [validators.DataRequired()])
    postal_code = StringField('Postal Code', [Length(6), validators.DataRequired()])
    email = EmailField('Email',  validators=[InputRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
    phone_number = StringField('Phone Number', [Length(8), validators.DataRequired()])

