import json
import os
import re

def parse_file(filename):
    pat = re.compile(r"([0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,2}.*?)(?=^^([0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,2}|\Z))",re.S | re.M)
    with open(filename,"r",encoding="utf8") as input:
        data = [m.group(1).strip().replace("\n",os.path.sep) for m in pat.finditer(input.read())]

    messeges =  {}

    for i,row in enumerate(data):
        try:
            splited = row.split(":")
            date = splited[0] + splited[1][:2]
            messege = splited[2]
        except:
            date = ''
            messege = ''
        if len(messege.split()) > 100:
            messeges[date] = messege

    return messeges
            
if __name__ == "__main__":
    messeges = parse_file("src.txt")
    #with open("out.txt","w",encoding="utf-8") as out:
    #    out.write(str(messeges))
    with open("out.json","w") as out:
        out.write(json.dumps(messeges,indent=2))