from pymongo import MongoClient
import json

client = MongoClient()
db = client["wordbase"]
collection = db["entries"]

language_counts = {}

for entry in collection.find():
    lang = entry["lang"]
    if lang not in language_counts:
        language_counts[lang] = 1
    else:
        language_counts[lang] += 1

languages = [{"language": lang, "wordsNum": count} for lang, count in language_counts.items()]

# sort the languages by the number of words in descending order
languages.sort(key=lambda x: x["wordsNum"], reverse=True)

with open("lexopedia-language-statistics.json", "w") as f:
    json.dump(languages, f)
