class Chat: #{id: Class(Chat .... [Class(Message)]}
    def __init__(self, id, sender, recipient): #init 3
        self.__id = id
        self.__sender = sender
        self.__recipient = recipient
        self.__messages = []
        self.__sender_status = "Pending"
        self.__recipient_status = ""

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_sender(self):
        return self.__sender

    def set_sender(self, sender):
        self.__sender = sender

    def get_recipient(self):
        return self.__recipient

    def set_recipient(self, recipient):
        self.__recipient = recipient

    def get_sender_status(self):
        return self.__sender_status

    def set_sender_status(self, sender_status):
        self.__sender_status = sender_status

    def get_recipient_status(self):
        return self.__recipient_status

    def set_recipient_status(self, recipient_status):
        self.__recipient_status = recipient_status

    def get_messages(self):
        return self.__messages

    def set_messages(self, messages):
        self.__messages.append(messages)

class Message:
    def __init__(self, message, sent_by, timestamp):
        self.__sent_by = sent_by
        self.__timestamp = timestamp
        self.__message = message

    def get_message(self):
        return self.__message

    def set_message(self, message):
        self.__message = message

    def get_timestamp(self):
        return self.__timestamp

    def set_timestamp(self, timestamp):
        self.__timestamp = timestamp

    def get_sent_by(self):
        return self.__sent_by

    def set_sent_by(self, sent_by):
        self.__sent_by = sent_by