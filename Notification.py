from datetime import datetime as dt

class Notification:
    def __init__(self, recipient, category, message, hyperlink):
        self.__hyperlink = hyperlink
        self.__category = category
        self.__message = message
        self.__recipient = recipient
        self.__id = 0
        self.__status = "new"
        self.__time = dt.today().strftime("%d %b %I:%M%p")

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_recipient(self):
        return self.__recipient

    def set_recipient(self, recipient):
        self.__recipient = recipient

    def get_message(self):
        return self.__message

    def set_message(self, message):
        self.__message = message

    def get_category(self):
        return self.__category

    def set_category(self, category):
        self.__category = category

    def get_hyperlink(self):
        return self.__hyperlink

    def set_hyperlink(self, hyperlink):
        self.__hyperlink = hyperlink

    def get_time(self):
        return self.__time

    def set_time(self, time):
        self.__time = time

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status