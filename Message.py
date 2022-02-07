'''
Message class
'''

from typing import Tuple
import hashlib

class Message():
    '''
    Message class for easier parsing and storing
    '''

    @staticmethod
    def parse(message: str) -> Tuple[str, str, str, str]:
        '''parses the message and returns the date, time, the number and the text'''
        try:
            splitted = message.split(":")
            if len(splitted) < 3:
                return "", "", "", message
            date = splitted[0][:-3].replace(",", "")
            time = splitted[0][-2:] + ":" + splitted[1][:2]
            num = "-".join(splitted[1].split("-")[1:]).strip()
            text = ":".join(splitted[2:])
            return date, time, num, text
        except IndexError:
            return "", "", "",  message

    def __init__(self, message: str):
        self.date, self.time, self.sender, self.text = Message.parse(message)

    @property
    def is_copypasta(self) -> bool:
        '''returns true if the message is a copypasta'''
        return len(self) > 100 or len(self.text) > 400

    @property
    def is_readable(self) -> bool:
        '''returns true if the message is readable'''
        return self.sender and self.text

    @property
    def hash(self) -> str:
        """
        Returns the sha1 of the text
        """
        return hashlib.sha1(self.text.encode()).hexdigest()

    def __len__(self) -> int:
        '''
        returns the num of words
        '''
        return len(self.text.split())

