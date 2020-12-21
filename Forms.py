from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, DateField
from datetime import date

class CreateAd(Form):
    startdate = DateField('Start Date:*', format='%d/%m/%Y')
    enddate = DateField('End Date:*', default=date.today, format='%d/%m/%Y')

    def compare_dates(self):
        result = super(CreateAd, self).validate()
        if (self.startdate.data > self.enddate.data):
            return False
