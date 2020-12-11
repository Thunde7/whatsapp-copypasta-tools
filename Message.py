class Message(object):
    @staticmethod
    def parse(message):
        try:
            splitted = message.split(":")
            if len(splitted) < 3:
                return None, None, message
            date_and_time = splitted[0] + ":" + splitted[1][:2]
            num = "-".join(splitted[1].split("-")[1:]).strip()
            text = ":".join(splitted[2:])
            return date_and_time, num, text
        except IndexError:
            return None, None, message

    def __init__(self, message):
        self.date_and_time, self.num, self.text = message.parse(message)

    def is_copypasta(self):
        return len(self) > 400 or len(self.text)

    def is_readable(self):
        return self.num is not None

    def __len__(self):
        '''
        returns the num of words
        '''
        return len(self.text.split())
