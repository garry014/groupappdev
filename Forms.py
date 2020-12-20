from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, DateField
from datetime import date

class createAd(Form):
    startdate = DateField('Start Date', default=date.today)
    enddate = DateField('End Date', default=date.today)

    def compare_dates(self):
        result = super(createAd, self).validate()
        if (self.startdate.data > self.enddate.data):
            return False
