from wtforms import Form, StringField, validators

class updateAvail(Form):
    availstart = StringField('Enter Start Time: ', [validators.DataRequired()])
    availend = StringField('Enter End Time: ', [validators.DataRequired()])


