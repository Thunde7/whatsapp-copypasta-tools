import sys
import utils


if __name__ == "__main__":
    big_data = set()
    for file in sys.argv[1:]:
        print(len(utils.read_from_json(file)))
        big_data |= set(utils.read_from_json(file))
        print(len(big_data))
    utils.write_messeges_to_json("huge_data.json",big_data)
    