class Vouchers:
    def __init__(self, code, description, discount, minpurchase, quantity, vstartdate, vexpirydate):
        self.__code = code
        self.__description = description
        self.__discount = discount
        self.__minpurchase = minpurchase
        self.__quantity = quantity
        self.__vstartdate = vstartdate
        self.__vexpirydate = vexpirydate
        self.__voucher_id = 0

    def get_code(self):
        return self.__code

    def set_code(self, code):
        self.__code = code

    def get_description(self):
        return self.__description

    def set_description(self, description):
        self.__description = description

    def get_discount(self):
        return self.__discount

    def set_discount(self, discount):
        self.__discount = discount

    def get_minpurchase(self):
        return self.__minpurchase

    def set_minpurchase(self, minpurchase):
        self.__minpurchase = minpurchase

    def get_quantity(self):
        return self.__quantity

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def get_vstartdate(self):
        return self.__vstartdate

    def set_vstartdate(self, vstartdate):
        self.__vstartdate = vstartdate

    def get_vexpirydate(self):
        return self.__vexpirydate

    def set_vexpirydate(self, vexpirydate):
        self.__vexpirydate = vexpirydate

    def get_voucher_id(self):
        return self.__voucher_id

    def set_voucher_id(self, voucher_id):
        self.__voucher_id = voucher_id
