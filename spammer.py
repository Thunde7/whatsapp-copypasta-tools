#########
#IMPORTS#
#########
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from string import ascii_letters, ascii_lowercase
import selenium

import pyperclip
import argparse
import random
import json
import time

import utils
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

parser.add_argument(
    "-n",
    "--name",
    required=True,
    help="the name of the victim"
)

parser.add_argument(
    "-p",
    "--path",
    required=False,
    help="path for the webdriver",
    default='C:\\webdrivers\\chromedriver.exe'
)

args = parser.parse_args()

def shuffle_from_file(dir):
    res = list(utils.read_from_json(dir))
    random.shuffle(res)
    return res

def get_random_word():
    return "".join(random.choice(ascii_letters) for _ in range(random.randint(3,10)))

def spam_maker(args):
    if args.json:
        spam = shuffle_from_file(args.json)
    elif args.text:
        spam = utils.read_from_text(args.text)
    else:
        spam = [" ".join(get_random_word() for _ in range(400)) for _ in range(2000)]
    return spam



chrome_options = Options()
chrome_options.add_argument("user-data-dir=selenium")   
driver = webdriver.Chrome(executable_path= args.path, options=chrome_options)
driver.get('https://web.whatsapp.com')

while True:
    try:
        driver.find_element_by_xpath(f'//*[@contenteditable = "true"]')
        break
    except selenium.common.exceptions.NoSuchElementException:
        continue
print("Connected successfully!")

def chat(name):
    try:
        driver.find_element_by_xpath(f'//span[@title="{name}"]').click()
        name=name
    except selenium.common.exceptions.NoSuchElementException:
        driver.close()
        raise Exception(f"No chat named {name}")

def send_message(msg):
    chat_box = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]')
    chat_box.click()
    chat_box.send_keys(msg+ Keys.ENTER)

#
#victim = input("who we spamming boissssssssss\n\n")
#driver.find_element_by_css_selector(f'span[title="{victim}"]').click()

chat(args.name)
for spam in spam_maker(args):
    send_message(spam)