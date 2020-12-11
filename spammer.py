#########
#IMPORTS#
#########
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as chOptions
from selenium.webdriver.firefox.options import Options as fiOptions
from string import ascii_letters
import selenium

import pyperclip
import argparse
import random
import time
import sys

import file_utils

######
#ARGS#
######
parser = argparse.ArgumentParser(
    description='Parsing Module for the bot',
    usage='python spammer.py [-d] [-t] [-j] [-n] [-p path] [-f -p path]',
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
    required=False,
    help="the name of the victim"
)

parser.add_argument(
    "-p",
    "--path",
    required=False,
    help="path for the webdriver",
    default='.\\drivers\\chromedriver.exe' if sys.platform == "win32" else './drivers/chromedriver'
)

parser.add_argument(
    '-f',
    '--firefox',
    required=False,
    help='use firefox instead of chrome',
    action="store_true"
)

args = parser.parse_args()


###########
#FUNCTIONS#
###########
def shuffle_from_file(dir):
    res = list(file_utils.read_from_json(dir))
    random.shuffle(res)
    return res


def get_random_word():
    return "".join(random.choice(ascii_letters) for _ in range(random.randint(3, 10)))


def spam_maker(args):
    if args.json:
        spam = shuffle_from_file(args.json)
    elif args.text:
        spam = file_utils.read_from_text(args.text)
    else:
        spam = [" ".join(get_random_word() for _ in range(400))
                for _ in range(2000)]
    return spam


if args.firefox:
    options = fiOptions()
    options.add_argument("user-data-dir=selenium")
    driver = webdriver.Firefox(executable_path=args.path, options=options)
else:
    options = chOptions()
    options.add_argument("user-data-dir=selenium")
    driver = webdriver.Chrome(executable_path=args.path, options=options)

driver.get('https://web.whatsapp.com')

while True:
    try:
        driver.find_element_by_xpath(f'//*[@contenteditable = "true"]')
        break
    except selenium.common.exceptions.NoSuchElementException:
        continue
print("Connected successfully!")
time.sleep(2)


def chat(name):
    try:
        driver.find_element_by_xpath(f'//span[@title="{name}"]').click()
        name = name
    except selenium.common.exceptions.NoSuchElementException:
        driver.close()
        raise Exception(f"No chat named {name}")


def send_message(msg):
    chat_box = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]')
    chat_box.click()
    pyperclip.copy(msg)
    chat_box.send_keys(Keys.CONTROL + "v")
    chat_box.send_keys(Keys.ENTER)


if __name__ == "__main__":
    if args.name is not None:
        chat(args.name)
    else:
        input(f"{50 * '='}\npress enter after you have chose the victim\n{50 * '='}\n")

    for spam in spam_maker(args):
        try:
            send_message(spam)
        except KeyboardInterrupt:
            driver.close()
        except Exception as ex:
            print(ex)
            driver.close()
