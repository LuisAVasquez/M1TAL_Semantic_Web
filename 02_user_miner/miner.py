
from datetime import *
from math import gamma
import os


def get_hour_minute_second_string():
    now = datetime.now()
    time = now.strftime("%H%M%S%M") + str(now.microsecond)
    time = str(time)
    return time

filename = "user_data_" + get_hour_minute_second_string() + '.csv'
data_path = 'user_data'

# will be saved to a csv
current_file_path = os.path.join(data_path, filename)


import random

import pandas as pd

end_message = " write 'next' to got to the next question, and 'exit' to quit"

def custom_ask(question_string, options_list = None):
    print(end_message)
    if options_list:
        print(*enumerate(options_list), sep = "\n")
    try:
        result = input(">>>" + question_string + ":  ")
    except:
        result = None
    return result

full_lists = {
    "games" : ["FIFA " + str(i) for i in range(1990, 2030)],
    "genres" : ["racing", "fights", "puzzle", "trivia", "fps", "strategy"],
    "consoles": ["PlayStation" + str(i)  for i in range(1, 20)],
    "languages": ["spanish", "portuguese", "french", "chinese", "greek"]
}


all_entries = []



while True:

    empty_entry = {
        "id": None, "name": None, "games" : [], "genres" : [],  "age": None, "consoles": [], "languages": []
    }

    print("\n"*2)
    print(">"*20)
    print("Adding one player to the database")
    print("<"*20)
    current_id = get_hour_minute_second_string()
    current_entry = empty_entry.copy()
    print(current_entry)
    current_entry["id"] = current_id

    # ask for age

    name = custom_ask("What is your name?")
    if name == 'next': 
        pass
    elif name == 'exit':
        all_entries.append(current_entry)
        break
    else:
        current_entry["name"] = name

    
    
    ## ask for the game

    idx = None
    while True:
        games_list = random.sample(full_lists["games"], 10)
        idx = custom_ask(name + ", which of this games do you play? (only index)" , games_list)
        if idx == 'next' or idx == 'exit': break
        idx = int(idx)
        game = games_list[idx]
        if game not in current_entry["games"]:
            current_entry["games"].append(game)

    if idx == 'next': pass
    if idx == 'exit': 
        all_entries.append(current_entry)
        break
    #print(current_entry)


    ## ask for the genres
    idx = None
    while True:
        genres_list = random.sample(full_lists["genres"], 3)
        idx = custom_ask(name + ", which of this genres do you play? (only index)" , genres_list)
        if idx == 'next' or idx == 'exit': break
        idx = int(idx)
        genre = genres_list[idx]
        if genre not in current_entry["genres"]:
            current_entry["genres"].append(genre)

    if idx == 'next': pass
    if idx == 'exit': 
        all_entries.append(current_entry)
        break
    #print(current_entry)
    
    ## ask for age


    age = custom_ask(name + ", what is your age?")
    if age == 'next': 
        pass
    elif age == 'exit':
        all_entries.append(current_entry)
        break
    else:
        age = int(age)
        current_entry["age"] = age

    ## ask for consoles

    idx = None
    while True:
        consoles_list = random.sample(full_lists["consoles"], 3)
        idx = custom_ask(name + ", which of this consoles do you have (only index)" , consoles_list)
        if idx == 'next' or idx == 'exit': break
        idx = int(idx)
        console = consoles_list[idx]
        if console not in current_entry["consoles"]:
            current_entry["consoles"].append(console)

    if idx == 'next': pass
    if idx == 'exit': 
        all_entries.append(current_entry)
        break
    #print(current_entry)

    ## ask for languages
    idx = None
    while True:
        language_list = random.sample(full_lists["languages"], 3)
        idx = custom_ask(name + ", which of this languages do you speak (only index)" , language_list)
        if idx == 'next' or idx == 'exit': break
        idx = int(idx)
        language = language_list[idx]
        if language not in current_entry["languages"]:
            current_entry["languages"].append(language)

    if idx == 'next': pass
    if idx == 'exit': 
        all_entries.append(current_entry)
        break

    all_entries.append(current_entry)

try:
    os.mkdir(data_path)
except:
    pass

print("Exiting... saving as CSV in ", current_file_path)

df = pd.DataFrame(all_entries)
df.to_csv(current_file_path)

print("Saved!")