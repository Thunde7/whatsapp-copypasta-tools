import argparse
import json

import utils

parser = argparse.ArgumentParser(
    description='Generate Pasta json from exported chat',
    usage='python gen_json.py INPUT OUTPUT [-d]'
)

parser.add_argument('src',
                    metavar='INPUT',
                    help='exported file'
                    )

parser.add_argument('out',
                    metavar='OUTPUT',
                    help='file to write results to'
                    )

parser.add_argument(
    "-d",
    "--debug",
    required=False,
    action="store_true",
    help="DEBUG mode, Enables prints"
)

if __name__ == "__main__":
    args = parser.parse_args()

    pasta_set = set()
    lost = 0

    for messege in utils.messeges_generator_from_file(args.src, args.debug):
        parsed = utils.parse_messege(messege)
        if parsed:
            date_and_time, number, text = parsed
            if utils.is_copypasta(text):
                pasta_set.add(text)
        else:
            lost += 1

    if args.debug:
        print(
            f"we didn't read {lost} of the messeges and {len(pasta_set)} of them were copypastas")

    utils.write_messeges_to_json(args.out, pasta_set)
