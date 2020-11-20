import argparse
import utils
from utils import is_copypasta


parser = argparse.ArgumentParser(
    description='stats module',
    usage='python stats.py INPUT [-d]'
)

parser.add_argument(
    "src",
    metavar="INPUT",
    help="the exported file"
)

parser.add_argument(
    "-d",
    "--debug",
    required=False,
    action='store_true',
    help="DEBUG mode, Enables prints"
)


if __name__ == "__main__":
    args = parser.parse_args()
    lost = 0
    pastas = 0
    
    stat_dict = dict()
    for messege in utils.messeges_generator_from_file(args.src,args.debug):
        parsed = utils.parse_messege(messege)
        if parsed:
            date_and_time,number,text = parsed
            pasta = utils.is_copypasta(text)
            utils.add_to_stats(stat_dict,number,pasta)
            if pasta:
                pastas += 1
        else:
            lost += 1
    
    if args.debug:
        print(f"we didn't read {lost} of the messeges and {pastas} of them were copypastas")

    utils.write_all_stats(stat_dict)
