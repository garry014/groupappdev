from wtforms import Form, StringField, validators

class updateAvail(Form):
    availstart = StringField('Enter Start Time (12H): ', [validators.DataRequired()])
    availend = StringField('Enter End Time (12H): ', [validators.DataRequired()])


