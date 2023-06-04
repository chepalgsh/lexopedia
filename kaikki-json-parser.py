import json
import re
from tqdm import tqdm

# Open the input and output files
with open('kaikki.org-dictionary-all.json', 'r', encoding='utf-8') as f_in, open('wordbase.json', 'w', encoding='utf-8') as f_out:

    # Define the regular expression pattern to match Latin characters
    latin_pattern = re.compile(r'^[a-zA-ZāēīōūȳǖÄÖÜäöüßẞÀàÁáÂâÃãÄäÅåÆæÇçÈèÉéÊêËëÌìÍíÎîÏïÐðÑñÒòÓóÔôÕõÖöØøŒœÞþÙùÚúÛûÜüÝýŸÿḪḫḨḩḤḥḪḫḨḩḤḥḰḱḲḳḴḵḶḷḺḻḼḽḸḹḼḽḾḿ]+$',
                               flags=re.UNICODE)

    # Create an empty list to store the parsed JSON objects
    output_list = []

    # Iterate over each line in the input file (each line is a JSON object)
    for line in tqdm(f_in, "Parsing kaikki dictionary"):

        # Load the JSON object
        obj = json.loads(line)

        # Check if the word field contains Latin characters
        if 'word' in obj and latin_pattern.match(obj['word']):
            
            # Extract only the necessary fields
            new_obj = {
                "word": obj["word"],
                "lang": obj["lang"],
                "glosses": []
            }

            # Extract glosses from each sense object if it exists
            for sense in obj["senses"]:
                if "glosses" in sense and len(sense["glosses"]) > 0:
                    for gloss in sense["glosses"]:
                        if len(gloss.split()) <= 3:
                            new_obj["glosses"].append(gloss)

            # Append the new JSON object to the list if it has at least one gloss
            if len(new_obj["glosses"]) > 0:
                output_list.append(new_obj)

    # Write the list of JSON objects to the output file
    json.dump(output_list, f_out)

    print("Parsing has been finished.")
