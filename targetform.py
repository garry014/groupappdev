from wtforms import Form, StringField, validators

class updateTarget(Form):
    target = StringField('Enter Target: ', [validators.DataRequired()])



