# whatsapp - copypasta related tools

this is a Python library for dealing with whatsapp exported files, and running statistics related specifically to copypastas.


## Usage

usage: 
```
python stats.py INPUT [-d]

stats module

positional arguments:
  INPUT        the exported file

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  DEBUG mode, Enables prints
```
or:

```
python gen_json.py INPUT OUTPUT [-d]

Generate Pasta json from exported chat

positional arguments:
  INPUT        exported file
  OUTPUT       file to write results to

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  DEBUG mode, Enables prints
```

alternatively, you can use:
```
python parser.py INPUT OUTPUT [-h] [-l] [-d] [-b] [-w]

Parsing Module for the bot

positional arguments:
  INPUT              exported file
  OUTPUT             file to writr results to

optional arguments:
  -h, --help         show this help message and exit
  -l, --leaderboard  Leaderboard generator
  -d, --debug        DEBUG MODE, Enables prints
  -b, --best         Find who sent most copypastas
  -w, --worst        Find who sent most non copypastas
```

Finally, you can use the spam module with:
```
python spammer.py [-d] [-t] [-j]

Parsing Module for the bot

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           DEBUG MODE, Enables prints
  -j JSON, --json JSON  the json file to read the spam from, should look somthing like this:
  {
      key_1 : spam_1,
      key_2 : spam_2,
      key_3 : spam_3,
      .
      .
      .
      key_n : spam_n
  }
  -t TEXT, --text TEXT  the text file to read the spam from, any text file will do
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

