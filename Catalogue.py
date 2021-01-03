class Catalouge:
    def __init__(self, id, name, price, discount, image, description, custom): #init 7, last one a dictionary, key question number, value - custom
        self.__id = id
        self.__name = name
        self.__price = price
        self.__discount = discount
        self.__image = image
        self.__description = description
        self.__reviews = 0
        self.__custom = custom

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

    def get_custom(self):
        return self.__custom

    def set_custom(self, custom):
        self.__custom = custom

class Customiseable():
    def __init__(self, question, choices, category): # Question to ask, Category: Radiobutton/String,etc, MCQ if applicable
        self.__category = category
        self.__choices = choices
        self.__question = question

    def get_category(self):
        return self.__category

    def set_category(self, category):
        self.__category = category

    def get_choices(self):
        return self.__choices

    def set_choices(self, choices):
        self.__choices = choices

    def get_question(self):
        return self.__question

    def set_question(self, question):
        self.__question = question






