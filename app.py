import math
from Levenshtein import distance
from flask import Flask, redirect, render_template, request, url_for
import jellyfish
from pymongo import MongoClient
import os
import pickle

app = Flask(__name__)

# Connect to the MongoDB database and select the "wordbase" collection
client = MongoClient()
db = client["wordbase"]
collection = db["entries"]

def find_meaning_matches(target_gloss):
    meaning_matches = []
    for entry in collection.find():
        for gloss in entry["glosses"]:
            gloss_words = gloss.lower().split()
            if target_gloss in gloss_words:
                distance_score = distance(gloss.lower(), target_gloss.lower())
                max_len = max(len(gloss), len(target_gloss))
                sim = 1 - distance_score / max_len
                if sim > 0.3:
                    meaning_matches.append((entry, gloss))
    
    # Sort meaning_matches alphabetically
    meaning_matches.sort(key=lambda x: x[0]["word"].lower())
    
    return meaning_matches


def find_spelling_matches(target_word):
    spelling_matches = []
    for entry in collection.find():
        word = entry['word']
        lang = entry['lang']
        gloss = entry['glosses'][0] if entry['glosses'] else ''
        if len(gloss.split()) > 0 and len(gloss.split()) <= 2 and word.startswith(target_word[0]):
            if target_word.startswith(word) and len(word) > 2:
                spelling_matches.insert(0, (word, lang, gloss))
            elif jellyfish.soundex(target_word) == jellyfish.soundex(word):
                spelling_matches.append((word, lang, gloss))
            elif word.startswith(target_word):
                spelling_matches.insert(0, (word, lang, gloss))
    return spelling_matches

def find_language_words(lang, page=1, page_size=100, chunk_size=1000):
    filepath = f"lexopedia-cache/dictionaries/{lang}/{lang}-{page}.pkl"
    if not os.path.exists(f"lexopedia-cache/dictionaries/{lang}"):
        os.makedirs(f"lexopedia-cache/dictionaries/{lang}")

    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            words = pickle.load(f)
    else:
        words = []

        # Calculate which chunk to retrieve for the current page
        chunk_num = (page - 1) // (page_size // chunk_size) + 1
        # Retrieve words for the current chunk
        start_index = (chunk_num - 1) * chunk_size
        end_index = start_index + chunk_size
        for entry in collection.find({"lang": lang}).skip(start_index).limit(chunk_size):
            word = entry['word']
            lang = entry['lang']
            gloss = entry['glosses'][0] if entry['glosses'] else ''
            if word not in words:
                words.append((word, lang, gloss))

        # Save words to cache file only if words are not empty
        if words:
            with open(filepath, "wb") as f:
                pickle.dump(words, f)

    # Calculate starting and ending index for the current page
    start_index = (page - 1) * page_size % chunk_size
    end_index = start_index + page_size

    # Retrieve words for the current page
    language_words = words[start_index:end_index]

    return language_words

def get_dictionary_num_pages(lang, page_size):
    total_words = collection.count_documents({"lang": lang})
    num_pages = (total_words + page_size - 1) // page_size
    return num_pages


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/dictionaries", methods=["GET"])
def dictionaries():
    return render_template("dictionaries.html")

@app.route("/nakh-and-indo-european", methods=["GET"])
def nakh_and_indoeuropean_similarities():
    return render_template("nakh-and-indo-european.html")

@app.route('/patrons')
def sponsors():
    patrons = []
    return render_template('patrons.html', patrons=patrons)

@app.route("/search", methods=["GET"])
def search():
    return render_template("search.html")

@app.route("/search-spelling-matches/", methods=["POST"])
def spelling_matches():
    if not os.path.exists("lexopedia-cache"):
      os.makedirs("lexopedia-cache")

    filename = f'{request.form["searchTerm"]}-spelling-matches'
    filepath = os.path.join("lexopedia-cache", filename)
    
    # Check if the file exists and redirect to the existing page if it does
    if os.path.exists(filepath):
      return redirect(f"/spelling-matches/{request.form['searchTerm'].lower()}")
    
    # Find words that are closest in spelling to the target word
    spelling_matches = find_spelling_matches(request.form["searchTerm"].lower())
    
    # Prepare the data to be passed to the HTML template
    spelling_matches_data = [(word, lang, glosses) for word, lang, glosses in spelling_matches]
    
    with open(filepath, "wb") as f:
        pickle.dump(spelling_matches_data, f)

    return redirect(f"/spelling-matches/{request.form['searchTerm'].lower()}")


@app.route("/spelling-matches/<searchTerm>")
def cached_spelling_matches(searchTerm):
    if not os.path.exists("lexopedia-cache"):
      os.makedirs("lexopedia-cache")
    # Check if a file with this name exists
    filename = f"{searchTerm.lower()}-spelling-matches"
    filepath = os.path.join("lexopedia-cache", filename)

    if os.path.exists(filepath):
        # Load the data from the file
        with open(filepath, "rb") as f:
            spelling_matches_data = pickle.load(f)
            languages = set(match[1] for match in spelling_matches_data)

        return render_template("cached_spelling_matches.html", spelling_matches=spelling_matches_data, languages=f"{len(languages)}", words=f"{len(spelling_matches_data)}", word=searchTerm.lower())

    return "No matches found for this word."

@app.route("/search-meaning-matches/", methods=["POST"])
def meaning_matches():
    if not os.path.exists("lexopedia-cache"):
      os.makedirs("lexopedia-cache")
    filename = f'{request.form["searchTerm"].lower()}-meaning-matches'
    filepath = os.path.join("lexopedia-cache", filename)
    
    # Check if the file exists and redirect to the existing page if it does
    if os.path.exists(filepath):
      return redirect(f"/meaning-matches/{request.form['searchTerm'].lower()}")

    # If the file doesn't exist, generate the matches and save them to the file
    meaning_matches = find_meaning_matches(request.form["searchTerm"].lower())
    
    meaning_matches_data = [(entry["word"], entry["lang"], gloss) for entry, gloss in meaning_matches]

    with open(filepath, "wb") as f:
        pickle.dump(meaning_matches_data, f)

    return redirect(f"/meaning-matches/{request.form['searchTerm'].lower()}")


@app.route("/meaning-matches/<searchTerm>")
def cached_meaning_matches(searchTerm):
    if not os.path.exists("lexopedia-cache"):
      os.makedirs("lexopedia-cache")
    # Check if a file with this name exists
    filename = f"{searchTerm.lower()}-meaning-matches"
    filepath = os.path.join("lexopedia-cache", filename)

    if os.path.exists(filepath):
        # Load the data from the file
        with open(filepath, "rb") as f:
            meaning_matches_data = pickle.load(f)
            languages = set(match[1] for match in meaning_matches_data)

        return render_template("cached_meaning_matches.html", meaning_matches=meaning_matches_data, languages=f"{len(languages)}", words=f"{len(meaning_matches_data)}", gloss=searchTerm.lower())

    return "No matches found for this gloss."

@app.route("/dictionary/<lang>/<int:page>")
def dictionary(lang, page):
    per_page = 100  # Number of words per page
    language_words = find_language_words(lang, page, per_page, per_page)

    if not language_words:
        return f"No such page found for {lang} language."

    language_words_data = [(word, lang, glosses) for word, lang, glosses in language_words]

    # Calculate previous and next pages
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if len(language_words) == per_page else None

    # Generate page numbers
    num_pages = get_dictionary_num_pages(lang, per_page)  # This function returns the total number of pages for the given language
    page_numbers = range(1, num_pages + 1)

    return render_template("dictionary.html",
                           language_words=language_words_data,
                           lang=lang,
                           page=page,
                           prev_page=prev_page,
                           next_page=next_page,
                           page_numbers=page_numbers,
                           num_pages=num_pages)


@app.route("/dictionary/<lang>")
def dictionary_redirect(lang):
    return redirect(f"/dictionary/{lang}/1")

if __name__ == "__main__":
    app.run(debug=False)