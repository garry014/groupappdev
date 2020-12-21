from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields.html5 import DateField
from datetime import date

class CreateAd(Form):
    startdate = DateField('Start Date:*', validators=[validators.DataRequired()]) #format='%Y-%m-%d'
    enddate = DateField('End Date:*', validators=[validators.DataRequired()])

    def compare_dates(self):
        # result = super(CreateAd, self).validate()
        pass
        # if (self.startdate.data > self.enddate.data):
        #     return False

