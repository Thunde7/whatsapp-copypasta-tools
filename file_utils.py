#########
#IMPORTS#
#########
from typing import Iterator, List
import json
import re

from Message import Message

message_RE = re.compile(
    r"(\d{1,2}[- . /]\d{1,2}[- . /]\d{1,2}.*?)(?=^^(\d{1,2}[- . /]\d{1,2}[- . /]\d{1,2}|\Z))", re.S | re.M)
# TODO
# EMOJI_RE = re.compile(r'\d+(.*?)[\u263a-\U0001f645]')


###########
#FUNCTIONS#
###########
def messages_generator_from_file(filename: str, debug: bool) -> Iterator[Message]:
    try:
        with open(filename, "r", encoding="utf-8") as input:
            messages = [m.group(1).strip()
                        for m in message_RE.finditer(input.read())]
        if debug:
            print(f"we found {len(messages)} possible messages!")

    except FileNotFoundError as e:
        print(f'FILE "{filename}" was not found')
        raise e

    for message in messages:
        yield Message(message)


def read_from_json(dir: str) -> List[str]:
    data = list()
    try:
        with open(dir, "r", encoding="utf-8") as input:
            data = json.load(input)
    except FileNotFoundError:
        print(f"trouble reading from {dir}")
    return data


def read_from_text(dir) -> List[str]:
    data = ""
    try:
        with open(dir, "r", encoding="utf-8") as input:
            data += input.read()
    except FileNotFoundError:
        print(f"trouble reading from {dir}")
    return data.split()


def write_messages_to_json(filename, messages) -> None:
    with open(filename, "w", encoding="utf-8") as out:
        out.write(json.dumps(list(messages), indent=2, ensure_ascii=False))
