import pymongo
import json

# Connect to the MongoDB client
client = pymongo.MongoClient('mongodb://localhost:27017/')

# Get the database and collection objects
db = client['wordbase']
collection = db['entries']

# Open the parsed JSON file
with open('wordbase.json', 'r', encoding='utf-8') as f:

    # Load the list of JSON objects
    data = json.load(f)

    # Insert each JSON object into the collection
    for obj in data:
        collection.insert_one(obj)

    print("Importing to MongoDB has been finished.")