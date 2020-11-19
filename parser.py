import argparse
import json
import sys
import re
import os

########
#CONSTS#
########
MESSEGE_RE = re.compile(r"(\d{1,2}\/\d{1,2}\/\d{1,2}.*?)(?=^^(\d{1,2}\/\d{1,2}\/\d{1,2}|\Z))",re.S | re.M)



######
#ARGS#
######
parser = argparse.ArgumentParser(
    description='Parsing Module for the bot',
    usage='python parser.py INPUT OUTPUT [-h] [-l] [-d]'
)

parser.add_argument('src',
    metavar='INPUT',
    help='exported file'
)

parser.add_argument('out',
    metavar='OUTPUT',
    help='file to writr results to'
)

parser.add_argument(
    '-l',
    '--leaderboard',
    required=False,
    help="Leaderboard generator"
)

parser.add_argument(
    '-d',
    '--debug',
    required=False,
    help='DEBUG MODE, Enables prints'
)

args = parser.parse_args()

######
#READ#
######
try:
    with open(args.src,"r",encoding="utf-8") as input:
        messeges = [m.group(1).strip().replace("\n",os.path.sep) for m in MESSEGE_RE.finditer(input.read())]
    if args.debug:
        print(f"we found {len(messeges)} possible messeges!")

except FileNotFoundError as e:
    print(f'FILE "{args.src}" was not found')
    sys.exit()


#######
#UTILS#
#######

def parse_messege(messege):
    try:
        splitted = messege.split(":")
        date_and_time = splitted[0] + ":" + splitted[1][:2]
        number = "-".join(splitted[1].split("-")[1:]).strip()
        text = splitted[2]
        return date_and_time,number,text

    except IndexError:
        return None
    

def is_long(text,size=50):
    return len(text.split()) > size

def add_to_stats(dic,number,is_copypasta):
    if number not in dic:
        dic[number] = {True : 0, False : 0}
    dic[number][is_copypasta] += 1

def calc_stats(dic):
    leaderboard = []
    for number,stats in dic.items():
        entry = (number,stats[True]/stats[False]) if stats[False] != 0 else (number,0)
        leaderboard.append(entry)
    leaderboard.sort(reverse=True,key=lambda x: x[1])
    return leaderboard


######
#MAIN#
######

if args.leaderboard:
    leads = {}

if args.debug:
    lost = 0


result = {}

for messege in messeges:
    parsed = parse_messege(messege)
    if parsed:
        date_and_time, number, text = parsed
        is_copypasta = is_long(text)
        if args.leaderboard:
            add_to_stats(leads,number,is_copypasta)
        if is_copypasta:
            result[date_and_time] = text
    elif args.debug: lost += 1

if args.debug:
    print(f"we didn't parse {lost} messeges!")

with open(args.out,"w",encoding="utf-8") as out:
    out.write(json.dumps(result,indent=2))

if args.leaderboard:
    with open("leads.txt","w",encoding="utf-8") as out:
        out.write("\n".join(f"{i+1} : {entry[0]} with a ratio of {entry[1]} copypastas per non pastas"
        for i, entry in enumerate(calc_stats(leads)) if entry[1] != 0.0))
