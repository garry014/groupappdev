class Orders:
    def __init__(self, cname, description, price, due_date):
        self.__cname = cname
        self.__description = description
        self.__price = price
        self.__due_date = due_date
        self.__order_id = 0

    def get_cname(self):
        return self.__cname

    def set_cname(self, cname):
        self.__cname = cname

    def get_description(self):
        return self.__description

    def set_description(self, description):
        self.__description = description

    def get_price(self):
        return self.__price

    def set_price(self, price):
        self.__price = price

    def get_due_date(self):
        return self.__due_date

    def set_due_date(self, due_date):
        self.__due_date = due_date

    def get_order_id(self):
        return self.__order_id

    def set_order_id(self, order_id):
        self.__order_id = order_id
