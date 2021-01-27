class Customer:
    count_id = 0

    def __init__(self, firstname, lastname, user_name, password, address1, address2, city, postal_code, gender, email, phone_number):
        Customer.count_id += 1
        self.__user_id = Customer.count_id
        self.__firstname = firstname
        self.__lastname = lastname
        self.__user_name = user_name
        self.__password = password
        self.__address1 = address1
        self.__address2 = address2
        self.__city = city
        self.__postal_code = postal_code
        self.__gender = gender
        self.__email = email
        self.__phone_number = phone_number

    def get_user_id(self):
        return self.__user_id

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def get_firstname(self):
        return self.__firstname

    def set_firstname(self, firstname):
        self.__firstname = firstname

    def get_lastname(self):
        return self.__lastname

    def set_lastname(self, lastname):
        self.__lastname = lastname

    def get_user_name(self):
        return self.__user_name

    def set_user_name(self, user_name):
        self.__user_name = user_name

    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = password

    def get_address1(self):
        return self.__address1

    def set_address1(self, address1):
        self.__address1 = address1

    def get_address2(self):
        return self.__address2

    def set_address2(self, address2):
        self.__address2 = address2

    def get_city(self):
        return self.__city

    def set_city(self, city):
        self.__city = city

    def get_postal_code(self):
        return self.__postal_code

    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code

    def get_gender(self):
        return self.__gender

    def set_gender(self, gender):
        self.__gender = gender

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_phone_number(self):
        return self.__phone_number

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

