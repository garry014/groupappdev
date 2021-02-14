class Cart:
    def __init__(self, title, tailor, price, courseid, customerid): #, keyid):
        self.__courseid = courseid
        self.__price = price
        self.__tailor = tailor
        self.__title = title
        self.__customerid = customerid
        #self.__keyid = keyid

    def get_courseid(self):
        return self.__courseid
    def set_courseid(self, courseid):
        self.__courseid = courseid

    def get_price(self):
        return self.__price
    def set_price(self, price):
        self.__price = price

    def get_tailor(self):
        return self.__tailor
    def set_tailor(self, tailor):
        self.__tailor = tailor

    def get_title(self):
        return self.__title
    def set_title(self, title):
        self.__title = title

    def get_customerid(self):
        return self.__customerid
    def set_customerid(self, customerid):
        self.__customerid = customerid

   #def get_keyid(self):
   #    return self.__keyid
   #def set_keyid(self, keyid):
   #    self.__keyid = keyid

