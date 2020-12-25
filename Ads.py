class Ads:
    def __init__(self, image, store_name, start_date, end_date): #init 3 attributes
        self.__ad_id = 0
        self.__image = image
        self.__store_name = store_name
        self.__end_date = end_date
        self.__start_date = start_date
        self.__status = "Pending Approval"

    def get_ad_id(self):
        return self.__ad_id

    def set_ad_id(self, ad_id):
        self.__ad_id = ad_id

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

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    def get_store_name(self):
        return self.__store_name

    def set_store_name(self, store_name):
        self.__store_name = store_name