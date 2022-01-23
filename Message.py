'''
Message class
'''

from typing import Tuple

class Message():
    '''
    Message class for easier parsing and storing
    '''

    @staticmethod
    def parse(message: str) -> Tuple[str, str, str]:
        '''parses the message and returns the date and time, the number and the text'''
        try:
            splitted = message.split(":")
            if len(splitted) < 3:
                return "", "", message
            date_and_time = splitted[0] + ":" + splitted[1][:2]
            num = "-".join(splitted[1].split("-")[1:]).strip()
            text = ":".join(splitted[2:])
            return date_and_time, num, text
        except IndexError:
            return "", "", message

    def __init__(self, message: str):
        self.date_and_time, self.sender, self.text = Message.parse(message)

    @property
    def is_copypasta(self) -> bool:
        '''returns true if the message is a copypasta'''
        return len(self) > 100 or len(self.text) > 400

    @property
    def is_readable(self) -> bool:
        '''returns true if the message is readable'''
        return self.sender is not None

    def __len__(self) -> int:
        '''
        returns the num of words
        '''
        return len(self.text.split())
