class Ads:
    def __init__(self, image, start_date, end_date):
        self.__status = "Pending Approval"
        self.__end_date = end_date
        self.__start_date = start_date
        self.__image = image

    def get_image(self):
        return self.__image

    def set_image(self, image):
        self.__image = image

    def get_start_date(self):
        return self.__start_date

    def set_start_date(self, start_date):
        self.__start_date = start_date

    def get_end_date(self):
        return self.__end_date

    def set_end_date(self, end_date):
        self.__end_date = end_date

    def get_end_date(self):
        return self.__end_date

    def set_end_date(self, status):
        self.__status = status
