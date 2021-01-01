class Catalouge:
    def __init__(self, id, name, price, discount, image, description): #init 6
        self.__id = id
        self.__name = name
        self.__price = price
        self.__discount = discount
        self.__image = image
        self.__description = description
        self.__reviews = 0

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_price(self):
        return self.__price

    def set_price(self, price):
        self.__price = price

    def get_image(self):
        return self.__image

    def set_image(self, image):
        self.__image = image

    def get_description(self):
        return self.__description

    def set_description(self, description):
        self.__description = description

    def get_reviews(self):
        return self.__reviews

    def set_reviews(self, reviews):
        self.__reviews = reviews

    def get_discount(self):
        return self.__discount

    def set_discount(self, discount):
        self.__discount = discount