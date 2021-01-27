class Course:
    def __init__(self, title, tailor, material, language, livecourse, note, price, tbnail):
        #, tbnail, , video, material, language, livecourse, note, price
        self.__courseid = 0
        self.__title = title
        self.__tbnail =  tbnail
        self.__tailor = tailor
        #self.__video = video
        self.__material = material
        self.__language = language
        self.__livecourse = livecourse
        self.__note = note
        self.__price = price

    def get_courseid(self):
        return self.__courseid
    def set_courseid(self, courseid):
        self.__courseid = courseid

    def get_title(self):
        return self.__title
    def set_title(self, title):
        self.__title = title

    def get_tbnail(self):
        return self.__tbnail
    def set_tbnail(self, tbnail):
        self.__tbnail = tbnail

    def get_tailor(self):
        return self.__tailor
    def set_tailor(self, tailor):
        self.__tailor = tailor

    #def get_video(self):
    #    return self.__video
    #def set_video(self, video):
    #    self.__video = video

    def get_material(self):
        return self.__material
    def set_material(self, material):
        self.__material = material

    def get_language(self):
        return self.__language
    def set_language(self, language):
        self.__language = language

    def get_livecourse(self):
        return self.__livecourse
    def set_livecourse(self, livecourse):
        self.__livecourse = livecourse

    def get_note(self):
        return self.__note
    def set_note(self, note):
        self.__note = note

    def get_price(self):
        return self.__price
    def set_price(self, price):
        self.__price = price
