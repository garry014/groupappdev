class Content:
    def __init__(self, topic, video, course):
        self.__topic = topic
        self.__video = video
        self.__course = course

    def get_topic(self):
        return self.__topic
    def set_topic(self, topic):
        self.__topic = topic

    def get_video(self):
        return self.__video
    def set_video(self, video):
        self.__video = video

    def get_course(self):
        return self.__course
    def set_course(self, course):
        self.__course = course