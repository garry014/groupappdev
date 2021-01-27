class Availability:
    def __init__(self,availstart, availend):
        self.__availstart = availstart
        self.__availend = availend
        self.__avail_id = 0

    def get_availstart(self):
        return self.__availstart

    def set_availstart(self, availstart):
        self.__availstart = availstart

    def get_availend(self):
        return self.__availend

    def set_availend(self, availend):
        self.__availend = availend

    def get_avail_id(self):
        return self.__avail_id

    def set_avail_id(self, avail_id):
        self.__avail_id = avail_id
