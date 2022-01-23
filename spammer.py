'''
Spammer module
'''

###########
# IMPORTS #
###########

import os
import pyperclip
import argparse
import random
import time

from typing import List
from string import ascii_letters

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as chOptions
from selenium.webdriver.firefox.options import Options as fiOptions

import file_utils

########
# ARGS #
########

def parse_args()-> argparse.Namespace:
    '''Parses the arguments'''
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
        default=os.path.join(os.path.dirname(__file__), 'drivers/chromedriver')
    )

    parser.add_argument(
        '-f',
        '--firefox',
        required=False,
        help='use firefox instead of chrome',
        action="store_true"
    )

    return parser.parse_args()

#############
# FUNCTIONS #
#############

def shuffle_from_file(filename: str) -> List[str]:
    '''Shuffles a list of strings from a file'''
    res = list(file_utils.read_from_json(filename))
    random.shuffle(res)
    return res


def generate_random_word():
    '''Generates a random word'''
    return "".join(random.choice(ascii_letters) for _ in range(random.randint(3, 10)))


def spam_maker(args: argparse.Namespace):
    '''Spams the chat with the messages from the file'''
    if args.json:
        spam = shuffle_from_file(args.json)
    elif args.text:
        spam = file_utils.read_from_text(args.text)
    else:
        spam = [" ".join(generate_random_word() for _ in range(400))
                for _ in range(2000)]
    return spam


def chat(name, driver: webdriver):
    '''Choose the victim'''
    try:
        driver.find_element_by_xpath(f'//span[@title="{name}"]').click()
    except selenium.common.exceptions.NoSuchElementException:
        driver.close()
        raise Exception(f"No chat named {name}") from None


def send_message(msg: str, driver: webdriver):
    '''Send the messages to the victim'''
    chat_box = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]')
    chat_box.click()
    pyperclip.copy(msg)
    chat_box.send_keys(Keys.CONTROL + "v")
    chat_box.send_keys(Keys.ENTER)


def main() -> None:
    '''Main function'''
    args = parse_args()

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
            driver.find_element_by_xpath('//*[@contenteditable = "true"]')
            break
        except selenium.common.exceptions.NoSuchElementException:
            continue
    print("Connected successfully!")
    time.sleep(2)

    if args.name is not None:
        chat(args.name, driver)
    else:
        input(f"{50 * '='}\npress enter after you have chose the victim\n{50 * '='}\n")

    for spam in spam_maker(args):
        try:
            send_message(spam, driver)
        except KeyboardInterrupt:
            driver.close()
        except Exception as ex:
            print(ex)
            driver.close()


if __name__ == "__main__":
    main()
