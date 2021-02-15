from wtforms import Form, StringField, IntegerField, validators

class addVoucher(Form):
    code = StringField('Voucher Code', [validators.DataRequired()])
    description = StringField('Description', [validators.DataRequired()])
    discount = IntegerField('Discount (%)', [validators.DataRequired()])
    minpurchase = IntegerField('Minimum Purchase ($)', [validators.DataRequired()])
    quantity = IntegerField('Quantity', [validators.DataRequired()])
    vstartdate = StringField('Start Date (DD/MM/YYYY)', [validators.DataRequired()])
    vexpirydate = StringField('Expiry Date (DD/MM/YYYY)', [validators.DataRequired()])

