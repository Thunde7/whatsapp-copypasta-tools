'''
Stats module
'''

###########
# IMPORTS #
###########
from dataclasses import dataclass
from typing import Dict, Generator, List, Tuple
import argparse

from message import Message
from file_utils import messages_generator_from_file

################
# Number Class #
################

@dataclass(order=True)
class Number():
    mobile: str
    copypastas: int = 0
    spam: int = 0

    @property
    def ratio(self) -> float:
        '''returns the ratio of spam to copypastas'''
        return self.copypastas / self.spam
    
    @property
    def ratio_str(self) -> str:
        '''returns a string with the raw ratio'''
        return f"{self.mobile} with a ratio of {self.ratio} copypastas to regular messages\n"

    def copypasta_str(self, pasta: bool = True) -> str:
        '''returns a string with the raw copypasta count'''
        return f"{self.mobile} has {self.copypastas} copypastas\n" if pasta else \
                f"{self.mobile} has {self.spam} spam messages\n"


########
# ARGS #
########

def parse_args() -> argparse.Namespace:
    '''parses the args'''
    parser = argparse.ArgumentParser(
        description='stats module',
        usage='python stats.py INPUT [-d]'
    )

    parser.add_argument(
        "src",
        metavar="INPUT",
        help="the exported file from whatsapp"
    )

    parser.add_argument(
        "-d",
        "--debug",
        required=False,
        action='store_true',
        help="DEBUG mode, Enables prints"
    )

    return parser.parse_args()

#############
# FUNCTIONS #
#############


def add_to_stats(stat_dict: Dict[str, Number],
                 message: Message) -> None:
    '''
    adds a message to the stats dict
    '''
    if message.sender not in stat_dict:
        stat_dict[message.sender] = Number(message.sender)
    if message.is_copypasta:
        stat_dict[message.sender].copypastas += 1
    else:
        stat_dict[message.sender].spam += 1


def sorted_stats(stat_list: List[Number]) -> \
        Generator[Tuple[int, Number], None, None]:
    '''sorts and returns the stats in a enumerated list'''
    yield from enumerate(sorted(stat_list, reverse=True, key=lambda number: number.ratio))



def write_all_stats(stat_dict: Dict[str, Number],
                    leaderboard_file: str = "leaderboard.txt",
                    most_cp_file: str = "most_copypastas.txt",
                    most_spam_file: str = "most_non_copypastas.txt"
                    ) -> None:
    '''
    writes all the stats to the a file
    '''
    with open(leaderboard_file, "w", encoding="utf-8") as out:
        number_list = list(stat_dict.values())
        for place, number in enumerate(sorted(number_list, reverse=True,
                                        key=lambda number: number.ratio), 1):
            out.write(f"{place=} : {number.ratio_str}")

    with open(most_cp_file, "w", encoding="utf-8") as out:
        for place, number in enumerate(sorted(number_list, reverse=True,
                                        key=lambda number: number.copypastas), 1):
            out.write(f"{place=} : {number.copypasta_str()}")

    with open(most_spam_file, "w", encoding="utf-8") as out:
        for place, number in enumerate(sorted(number_list, reverse=True,
                                        key=lambda number: number.spam), 1):
            out.write(f"{place=} : {number.copypasta_str(pasta=False)}")


def main() -> None:
    '''main function'''
    args: argparse.Namespace = parse_args()

    lost: int = 0
    pastas: int = 0

    stat_dict: Dict[str, Number] = {}
    for message in messages_generator_from_file(args.src, args.debug):
        if message.is_readable:
            add_to_stats(stat_dict, message)
            if message.is_copypasta:
                pastas += 1
        else:
            lost += 1

    if args.debug:
        print(
            f"we didn't read {lost} of the messages and {pastas} of them were copypastas")

    write_all_stats(stat_dict)


if __name__ == "__main__":
    main()
