from datetime import datetime as dt

class Reviews:
    def __init__(self, id, storename, productid, username, stars, review, photo):
        self.__username = username
        self.__productid = productid
        self.__storename = storename
        self.__photo = photo
        self.__review = review
        self.__stars = stars
        self.__id = id
        self.__timestamp = dt.today().strftime("%d %b %I:%M%p")

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_storename(self):
        return self.__storename

    def set_storename(self, storename):
        self.__storename = storename

    def get_productid(self):
        return self.__productid

    def set_productid(self, productid):
        self.__productid = productid

    def get_stars(self):
        return self.__stars

    def set_stars(self, stars):
        self.__stars = stars

    def get_review(self):
        return self.__review

    def set_review(self, review):
        self.__review = review

    def get_photo(self):
        return self.__photo

    def set_photo(self, photo):
        self.__photo = photo

    def get_timestamp(self):
        return self.__timestamp

    def set_timestamp(self, timestamp):
        self.__timestamp = timestamp

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username