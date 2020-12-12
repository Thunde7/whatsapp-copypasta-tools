#########
#IMPORTS#
#########
from typing import Dict, List
import json
import argparse

from Message import Message
from file_utils import messages_generator_from_file

######
#ARGS#
######
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

###########
#FUNCTIONS#
###########

def add_to_stats(stat_dict: Dict[str, Dict[bool, int]],
                 message: Message) -> None:
    if message.num not in stat_dict:
        stat_dict[message.num] = {True: 0, False: 0}
    stat_dict[message.num][message.is_copypasta()] += 1


def stat_to_ratio(x, y): return x / y if y != 0 else x


def sorted_stats(stat_list: List[tuple[str, float]]) -> List[tuple[int, tuple[str, float]]]:
    return enumerate(sorted(stat_list, reverse=True, key=lambda item: item[1]))


def ratios_from_stats(stat_dict: Dict[str, Dict[bool, int]]) -> List[tuple[int, tuple[str, float]]]:
    ratio_dict = {}
    for num, copypasta_count_dict in stat_dict.items():
        ratio_dict[num] = stat_to_ratio(
            copypasta_count_dict[True], copypasta_count_dict[False])
    yield from sorted_stats(ratio_dict)


def order_stats_by_cp(stat_dict: Dict[str, Dict[bool, int]], copypasta: bool) -> list[tuple[int, tuple[str, float]]]:
    copypasta_stat_dict = {}
    for num, copypasta_cout_dict in stat_dict.items():
        copypasta_cout_dict[num] = copypasta_cout_dict[copypasta]
    yield from sorted_stats(copypasta_stat_dict)


def raw_ratios(placement, num, ratio) -> str:
    return f"{placement}: {num} with a ratio of {ratio} copypastas to regular messages\n"


def raw_copypasta(placment, num, amount, type) -> str:
    return f"{placment}: {num} with {amount} {type} copypastas\n"


def write_all_stats(stat_dict) -> None:
    with open("leaderboard.txt", "w", encoding="utf-8") as out:
        for place, num, ratio in ratios_from_stats(stat_dict):
            out.write(raw_ratios(place + 1, num, ratio))

    with open("most_copypastas.txt", "w", encoding="utf-8") as out:
        for place, num, cp_amount in order_stats_by_cp(stat_dict, True):
            out.write(raw_copypasta(place + 1, num, cp_amount, True))

    with open("most_non_copypastas.txt", "w", encoding="utf-8") as out:
        for place, num, cp_amount in order_stats_by_cp(stat_dict, False):
            out.write(raw_copypasta(place + 1, num, cp_amount, False))


if __name__ == "__main__":
    args = parser.parse_args()
    lost = 0
    pastas = 0

    stat_dict = dict()
    for message in messages_generator_from_file(args.src, args.debug):
        if message.is_readable():
            add_to_stats(stat_dict, message)
            if message.is_copypasta:
                pastas += 1
        else:
            lost += 1

    if args.debug:
        print(
            f"we didn't read {lost} of the messages and {pastas} of them were copypastas")

    write_all_stats(stat_dict)
