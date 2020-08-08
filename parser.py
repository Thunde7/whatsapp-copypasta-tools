import json
import io
import re

def parse_file(filename):
    pat = re.compile(r"([0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,2}.*?)(?=^^([0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,2}|\Z))",re.S | re.M)
    with io.open(filename,"r",encoding="utf8") as input:
        data = [m.group(1).strip() for m in pat.finditer(input.read())]

    messeges =  []

    for i,row in enumerate(data):
        try:
            messege = row.split(":")[2]
        except:
            messege = ''
        if len(messege.split()) > 100:
            messeges.append(messege)

    return messeges
            
if __name__ == "__main__":
    messeges = parse_file("src.txt")
    with io.open("out.json","w",encoding="utf8") as out:
        out.write(json.dumps({"messegs" : messeges},indent=2))
