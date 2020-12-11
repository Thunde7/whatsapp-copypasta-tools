# whatsapp - copypasta related tools

this is a Python library for dealing with whatsapp exported files, and running statistics related specifically to copypastas.


## Usage

usage: 
```
python stats.py INPUT [-d]

stats module

positional arguments:
  INPUT        the exported file from whatsapp

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  DEBUG mode, Enables prints
```
and you will get three files with rankings related to best copypasta/noncopypasta ratio, most copypastas and most not copypastas


or:

```
python gen_json.py INPUT OUTPUT [-d]

Generate Pasta json from exported chat

positional arguments:
  INPUT        the exported file from whatsapp
  OUTPUT       file to write results to

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  DEBUG mode, Enables prints
```
and you will get a json file with all the copypastas from you whatsapp export, in the following format:

```
[
      spam_1,
      spam_2,
      spam_3,
      .
      .
      .
      spam_n
  ]
```




Finally, you can use the spam module with:
```
python spammer.py [-d] [-t] [-j]

Parsing Module for the bot

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           DEBUG MODE, Enables prints
  -j JSON, --json JSON  the json file to read the spam from, should look somthing like this:
  [
      spam_1,
      spam_2,
      spam_3,
      .
      .
      .
      spam_n
  ]
  -t TEXT, --text TEXT  the text file to read the spam from, any text file will do
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

