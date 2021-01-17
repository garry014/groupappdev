class Rider:
    count_id = 0

    def __init__(self, firstname, lastname, user_name, password, email, phone_number, gender, transport, license_number):
        Rider.count_id += 1
        self.__user_id = Rider.count_id
        self.__firstname = firstname
        self.__lastname = lastname
        self.__user_name = user_name
        self.__password = password
        self.__email = email
        self.__phone_number = phone_number
        self.__gender = gender
        self.__transport = transport
        self.__license_number = license_number

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

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_phone_number(self):
        return self.__phone_number

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def get_gender(self):
        return self.__gender

    def set_gender(self, gender):
        self.__gender = gender

    def get_transport(self):
        return self.__transport

    def set_transport(self, transport):
        self.__transport = transport

    def get_license_number(self):
        return self.__license_number

    def set_license_number(self, license_number):
        self.__license_number = license_number


