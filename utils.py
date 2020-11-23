import json
import re


MESSEGE_RE = re.compile(r"(\d{1,2}\/\d{1,2}\/\d{1,2}.*?)(?=^^(\d{1,2}\/\d{1,2}\/\d{1,2}|\Z))",re.S | re.M)
# TODO
# EMOJI_RE = re.compile(r'\d+(.*?)[\u263a-\U0001f645]')

def messeges_generator_from_file(filename,debug):
    try:
        with open(filename,"r",encoding="utf-8") as input:
            messeges = [m.group(1).strip()#.replace("\n",os.path.sep)
                        for m in MESSEGE_RE.finditer(input.read())]
        if debug:
            print(f"we found {len(messeges)} possible messeges!")

    except FileNotFoundError as e:
        print(f'FILE "{filename}" was not found')
        raise e

    yield from messeges


def parse_messege(messege):
    try:
        splitted = messege.split(":")
        if len(splitted) < 3:
            raise IndexError
        date_and_time = splitted[0] + ":" + splitted[1][:2]
        number = "-".join(splitted[1].split("-")[1:]).strip()
        text = ":".join(splitted[2:])
        return date_and_time,number,text

    except IndexError:
        return None
    
def is_copypasta(text,min_len=100):
    #TODO add emoji support
    return len(text.split()) > min_len or len(text) > 4 * min_len

def add_to_stats(stat_dict,key,truth_value):
    if key not in stat_dict:
        stat_dict[key] = {True : 0, False : 0}
    stat_dict[key][truth_value] += 1


stat_to_ratio = lambda x,y : x / y if y != 0 else x 

def calc_ratios_from_stats(stat_dict):
    yield from sorted([(key,stat_to_ratio(value[True],value[False])) for key, value in stat_dict.items()],reverse=True,key=lambda item : item[1])

def calc_stats_order_by_true(stat_dict):
    yield from sorted([(key,value[True]) for key, value in stat_dict.items()],reverse=True,key=lambda item : item[1])

def calc_stats_order_by_false(stat_dict):
    yield from sorted([(key,value[False]) for key, value in stat_dict.items()],reverse=True,key=lambda item : item[1])

def write_messeges_to_json(filename,messeges):
    with open(filename,"w",encoding="utf-8") as out:
        out.write(json.dumps(list(messeges),indent=2,ensure_ascii=False))

def write_all_stats(stat_dict):
    with open("leaderboard.txt","w",encoding="utf-8") as out:
        out.write("\n".join(f"{i+1}: {entry[0]} with a ratio of {entry[1]} copypastas to regular messeges"
                for i,entry in enumerate(calc_ratios_from_stats(stat_dict)) if entry[1] != 0))
    with open("most_copypastas.txt","w",encoding="utf-8") as out:
        out.write("\n".join(f"{i+1}: {entry[0]} with {entry[1]} copypastas" 
                for i,entry in enumerate(calc_stats_order_by_true(stat_dict)) if entry[1] != 0))
    with open("most_non_copypastas.txt","w",encoding="utf-8") as out:
        out.write("\n".join(f"{i+1}: {entry[0]} with {entry[1]} non copypastas" 
                for i,entry in enumerate(calc_stats_order_by_false(stat_dict)) if entry[1] != 0))    


def read_from_json(dir):
    data = list()
    try:
        with open(dir,"r",encoding="utf-8") as input:
            data = json.load(input)
    except FileNotFoundError:
        print(f"trouble reading from {dir}")
    return data

def read_from_text(dir):
    data = ""
    try:
        with open(dir,"r",encoding="utf-8") as input:
            data += input.read()
    except FileNotFoundError:
        print(f"trouble reading from {dir}")
    return data.split()
