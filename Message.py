from typing import Tuple


class Message(object):
    @staticmethod
    def parse(message: str) -> Tuple[str, str, str]:
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

    def __init__(self, message: str):
        self.date_and_time, self.num, self.text = Message.parse(message)

    def is_copypasta(self) -> bool:
        return len(self) > 100 or len(self.text) > 400

    def is_readable(self) -> bool:
        return self.num is not None

    def __len__(self) -> int:
        '''
        returns the num of words
        '''
        return len(self.text.split())
