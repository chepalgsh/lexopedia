# [lexopedia.ru](https://lexopedia.ru)

![lexopedia ru](https://github.com/chepalgsh/lexopedia/assets/67635401/3d401ba6-aed4-488f-9a72-a66d9d602d6d)

Lexopedia is a comprehensive online tool that allows users to search for meaning or spelling matches between a vast number of languages, including old and new languages. It is based on [wiktionary.org](https://www.wiktionary.org) dumps from [kaikki.org](https://kaikki.org)

# Features
* User-friendly interface
* Dictionaries for over a thousand languages, including Latin, Gothic, Proto-Indo-European, Proto-Mongolic, Proto-Italian and Egyptian
* Easy-to-use search bar for finding meaning or spelling matches

# Why Lexopedia?
Lexopedia has a great potential to lead to groundbreaking linguistic breakthroughs by uncovering hidden lexical similarities between diverse languages.

# Installation
* To set up Lexopedia on your local computer, you need to follow these steps:

First you should download the dump file to the project directory from [kaikki.org](https://kaikki.org)

```

You need the one with all languages combined, it should be available on https://kaikki.org/dictionary/All%20languages%20combined/

```

After that you should use "requirements.txt" to install all requirement packages.

```

 pip install -r requirements.txt

```

Then you should run "kaikki-json-parser.py". This will save words and their meanings in a new JSON file while also removing all non-Latin written words.

```

python kaikki-json-parser.py

```

After that you should run "kaikki-json-to-mongo-loader.py". This will load newly parsed json file to the mongo database.

```

python kaikki-json-to-mongo-loader.py

```

Now you can run "app.py". This will make Lexopedia available on localhost for use.

```

"python app.py"

```

# How to Use
Lexopedia is super easy to use. Open Lexopedia on your web browser and type in the word you are looking for in the search bar. You can use the search bar to find meaning or spelling matches across more then a thousand languages.

# Conclusion
Lexopedia is an amazing tool for language lovers and linguistics enthusiasts. With its easy-to-use interface, and wide range of dictionaries for many languages, Lexopedia is a one-stop solution for all the nerds like me searching for hidden conections between unrelated languages.

You can view a list of our generous donors [here](https://lexopedia.ru/patrons)

<a href="https://www.buymeacoffee.com/lexopedia"><img src="https://img.buymeacoffee.com/button-api/?text=Buy us a pizza!&emoji=🍕&slug=lexopedia&button_colour=800000&font_colour=ffffff&font_family=Comic&outline_colour=ffffff&coffee_colour=FFDD00" /></a>
