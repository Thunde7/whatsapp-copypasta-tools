'''
Some file utils
'''

###########
# IMPORTS #
###########

from typing import Iterator, List
import json
import re

from message import Message

message_RE = re.compile(
    r"(\d{1,2}[- . /]\d{1,2}[- . /]\d{1,2}.*?)(?=^^(\d{1,2}[- . /]\d{1,2}[- . /]\d{1,2}|\Z))",
    re.S | re.M)
# TO DO fuck you pylint :/
# EMOJI_RE = re.compile(r'\d+(.*?)[\u263a-\U0001f645]')


#############
# FUNCTIONS #
#############

def messages_generator_from_file(filename: str, debug: bool) -> Iterator[Message]:
    '''
    Generator that yields messages from a file
    '''
    try:
        with open(filename, "r", encoding="utf-8") as in_file:
            messages = [m.group(1).strip()
                        for m in message_RE.finditer(in_file.read())]
        if debug:
            print(f"we found {len(messages)} possible messages!")

    except FileNotFoundError as exp:
        print(f'FILE "{filename}" was not found')
        raise exp

    for message in messages:
        yield Message(message)


def read_from_json(filename: str) -> List[str]:
    '''
    Read from a json file
    '''
    data = []
    try:
        with open(filename, "r", encoding="utf-8") as in_file:
            data = json.load(in_file)
    except FileNotFoundError:
        print(f"trouble reading from {filename}")
    return data


def read_from_text(filename) -> List[str]:
    '''
    Read from a text file
    '''
    data = ""
    try:
        with open(filename, "r", encoding="utf-8") as infile:
            data += infile.read()
    except FileNotFoundError:
        print(f"trouble reading from {filename}")
    return data.split()


def write_messages_to_json(filename, messages) -> None:
    '''
    Write messages to a json file
    '''
    with open(filename, "w", encoding="utf-8") as out:
        out.write(json.dumps(list(messages), indent=2, ensure_ascii=False))
