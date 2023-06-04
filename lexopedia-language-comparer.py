import jellyfish
from pymongo import MongoClient
from tqdm import tqdm

client = MongoClient()
db = client["wordbase"]
collection = db["entries"]

def find_meaning_matches(target_gloss, lang1, lang2):
    matches_lang1 = []
    matches_lang2 = []
    
    # Find all entries in lang1 and lang2 with the given gloss
    for entry in tqdm(collection.find({"$or": [{"lang": lang1}, {"lang": lang2}]}), desc="Finding entries"):
        for gloss in entry["glosses"]:
            gloss_words = gloss.lower().split()
            if target_gloss in gloss_words:
                if entry["lang"] == lang1:
                    matches_lang1.append((entry["word"], gloss))
                else:
                    matches_lang2.append((entry["word"], gloss))
    
    # Find all words with the same meaning in lang1 and lang2
    meaning_matches = []
    for word1, gloss1 in tqdm(matches_lang1, desc="Finding meaning matches"):
        for word2, gloss2 in matches_lang2:
            if gloss1 == gloss2:
                meaning_matches.append((word1, word2, gloss1))
                break
                
    return meaning_matches

def find_spelling_matches(word, lang):
    spelling_matches = []
    for entry in tqdm(collection.find({"lang": lang}), desc="Finding spelling matches"):
        entry_word = entry["word"]
        entry_gloss = entry["glosses"][0] if entry["glosses"] else ''
        if len(entry_gloss.split()) > 0 and len(entry_gloss.split()) <= 2 and entry_word.startswith(word[0]):
            if word.startswith(entry_word) and len(entry_word) > 2:
                spelling_matches.insert(0, (entry_word, entry_gloss))
            elif jellyfish.soundex(word) == jellyfish.soundex(entry_word):
                spelling_matches.append((entry_word, entry_gloss))
            elif entry_word.startswith(word):
                spelling_matches.insert(0, (entry_word, entry_gloss))
    return spelling_matches

def find_lexical_similarities(lang1, lang2):
    # Find all words in lang1 that have spelling matches in lang2
    similarities = []
    for entry in tqdm(collection.find({"lang": lang1}), desc="Finding lexical similarities"):
        word = entry["word"]
        spelling_matches = find_spelling_matches(word, lang2)
        for match_word, match_gloss in spelling_matches:
            similarities.append((word + " (" + lang1 + ")", match_word + " (" + lang2 + ")",
                                 match_gloss + " # " + entry["glosses"][0]))
    
    # Find lexical similarities between lang1 and lang2 using the meaning_matches
    for target_gloss in tqdm(set([match[2] for match in similarities]), desc="Finding meaning matches"):
        meaning_matches = find_meaning_matches(target_gloss, lang1, lang2)
        for match in meaning_matches:
            if match[0] + " (" + lang1 + ")" in [sim[0] for sim in similarities]:
                continue
            if match[1] + " (" + lang2 + ")" in [sim[1] for sim in similarities]:
                continue
            similarities.append((match[0] + " (" + lang1 + ")", match[1] + " (" + lang2 + ")", match[2]))
    
    # Write similarities to a text file
    with open(lang1 + "_" + lang2 + "_similarities.txt", "w") as f:
        for similarity in similarities:
            f.write(similarity[0] + " - " + similarity[1] + " # " + similarity[2] + "\n")
    
    return similarities

find_lexical_similarities("Proto-Nakh", "Proto-Celtic")
