class Target:
    def __init__(self,target):
        self.__target = target
        self.__target_id = 0

    def get_target(self):
        return self.__target

    def set_target(self, target):
        self.__target = target

    def get_target_id(self):
        return self.__target_id

    def set_target_id(self, target_id):
        self.__target_id = target_id
