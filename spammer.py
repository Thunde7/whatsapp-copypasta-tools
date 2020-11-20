#########
#IMPORTS#
#########
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from string import ascii_lowercase

import pyperclip
import argparse
import random
import json

######
#ARGS#
######
parser = argparse.ArgumentParser(
    description='Parsing Module for the bot',
    usage='python spammer.py [-d] [-t] [-j]',
)

parser.add_argument(
    '-d',
    '--debug',
    required=False,
    help='DEBUG MODE, Enables prints',
    action="store_true"
)

parser.add_argument(
    "-j",
    "--json",
    required=False,
    help="the json file to read the spam from"
)

parser.add_argument(
    "-t",
    "--text",
    required=False,
    help="the text file to read the spam from"
)

args = parser.parse_args()

def read_from_json(dir):
    data = {}
    try:
        with open(dir,"r",encoding="utf-8") as input:
            data = json.load(input)
    except FileNotFoundError:
        print(f"trouble reading from {dir}")
    res = data.values()
    random.shuffle(res)
    return res

def read_from_text(dir):
    data = ""
    try:
        with open(dir,"r",encoding="utf-8") as input:
            data += input.read()
    except FileNotFoundError:
        print(f"trouble reading from {dir}")
    return data.split()

def spam_generator(args):
    if args.json:
        yield from read_from_json(args.json)
    elif args.text:
        yield from read_from_text(args.text)
    else:
        i = 0
        while i < 100:
            yield "".join(random.choice(ascii_lowercase) for _ in range(12))
            i += 1


driver = webdriver.Chrome('C:\\webdrivers\\chromedriver.exe')
driver.implicitly_wait(20) 
driver.get('https://web.whatsapp.com')
input(f"{50 * '='}\npress enter after you have scanned the QR\n{50 * '='}\n")

#
#victim = input("who we spamming boissssssssss\n\n")
#driver.find_element_by_css_selector(f'span[title="{victim}"]').click()
input(f"{50 * '='}\npress enter after you have chose the victim\n{50 * '='}\n")

for spam in spam_generator(args):
    pyperclip.copy(spam)
    driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]').send_keys(Keys.CONTROL,"v")
    driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button').click()