import json
import os
import SPARQLWrapper
import random
from time import sleep

testFlag = False

endpoint_url = "http://10.11.120.183:9999/blazegraph/namespace/swproj/sparql"

def test_print(*args):
    if testFlag:
        print(*args)
    else:
        pass

######

# Load dictionaries with wikidata IDs and labels

######
dictionaries_path = "dictionaries/"

gameLabels_path = os.path.join(dictionaries_path, "game.json")
with open(gameLabels_path, 'r') as file:
    gameLabels = json.load(file)

genreLabels_path = os.path.join(dictionaries_path, "genre.json")

with open(genreLabels_path, 'r') as file:
    genreLabels = json.load(file)


platformLabels_path = os.path.join(dictionaries_path, "platform.json")

with open(platformLabels_path, 'r') as file:
    platformLabels = json.load(file)



######

# Request user data

######

def custom_ask(question):
    result = input(">>> " + question + " :")
    return result

def input_user_name():

    name = custom_ask("What's your name?")

    return name

def input_user_age(name):
    age = custom_ask("{name}, what's your age?".format(name=name))
    age = int(age)

    return age

def input_user_game(name):

    count = 0
    max_count = 3
    selected_gameIDs = []

    while count < max_count:
        
        # pick 10 games at random
        random_gameIDs_idx = random.sample(range(len(gameLabels)), 10)

        random_gameIDs = [ list(gameLabels.keys())[idx] for idx in random_gameIDs_idx]
        random_game_labels = [gameLabels[gameID] for gameID in random_gameIDs]
        
        
        print(*enumerate(random_game_labels), sep = "\n")
        print("{name}, which of these games do you like? (write the index)".format(name = name))
        print("write 'none' to get a new list!")
        idx = custom_ask("")
        
        if idx != "none":
            idx = int(idx)
            selected_gameID = random_gameIDs[idx]
            selected_gameIDs.append(selected_gameID)
            count += 1
    
    return selected_gameIDs


def input_user_platform(name):

    count = 0
    max_count = 3
    selected_platformIDs = []
    
    while count < max_count:
        
        # pick 10 platforms at random
        random_platformIDs_idx = random.sample(range(len(platformLabels)), 10)

        random_platformIDs = [ list(platformLabels.keys())[idx] for idx in random_platformIDs_idx]
        random_platform_labels = [platformLabels[platformID] for platformID in random_platformIDs]
        
        
        print(*enumerate(random_platform_labels), sep = "\n")
        print("{name}, which of these platforms do you have? (write the index)".format(name = name))
        print("write 'none' to get a new list!")
        idx = custom_ask("")
        
        if idx != "none":
            idx = int(idx)
            selected_platformID = random_platformIDs[idx]
            selected_platformIDs.append(selected_platformID)
            count += 1
    
    return selected_platformIDs

def input_user_genre(name):

    count = 0
    max_count = 3
    selected_platformIDs = []
    
    while count < max_count:
        
        # pick 10 platforms at random
        random_platformIDs_idx = random.sample(range(len(genreLabels)), 10)

        random_platformIDs = [ list(genreLabels.keys())[idx] for idx in random_platformIDs_idx]
        random_platform_labels = [genreLabels[platformID] for platformID in random_platformIDs]
        
        
        print(*enumerate(random_platform_labels), sep = "\n")
        print("{name}, which of these genres do you like? (write the index)".format(name = name))
        print("write 'none' to get a new list!")
        idx = custom_ask("")
        
        if idx != "none":
            idx = int(idx)
            selected_platformID = random_platformIDs[idx]
            selected_platformIDs.append(selected_platformID)
            count += 1
    
    return selected_platformIDs



print("-"*20)
print("Hello, welcome to our game recommendator!")
print("-"*20)

sleep(1)

userName = input_user_name()
userAge = input_user_age(userName)
userGameIDs = input_user_game(userName)
userPlatformIDs = input_user_platform(userName)
userGenreIDs  = input_user_genre(userName)


sleep(1)

if testFlag:
    print("test logs:")
    print(userName, userAge, userGameIDs, sep="\n---\n---\n")



#####

# Quering our triple store

#####

print("Querying....")

from SPARQLWrapper import SPARQLWrapper, JSON, XML, TURTLE, RDF, CSV
import sys



def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    #sparql.setReturnFormat(XML)
    return sparql.query().convert()


def query_triplestore_byGameAndAge(gameID, userAge):


    query = """PREFIX wd: <http://www.wikidata.org/entity/> 
    prefix : <http://www.example.org/semanticwebproject#>

    SELECT ?recGameID 
    WHERE {

    %s :hasGenre ?genreID.
    %s :onPlatform ?platformID.
    ?recGameID :onPlatform ?platformID.
    ?recGameID :hasGenre ?genreID.
    ?recGameID :hasPegi ?pegi

    FILTER (%s != ?recGameID)
    FILTER (%d >= ?pegi)
    }
    """ % (
        gameID, 
        gameID, 
        gameID, 
        userAge
        )
    results = get_results(endpoint_url, query)
    results = results['results']['bindings']
    results = [elem['recGameID']['value'] for elem in results]
    results = ["wd:" + elem.rsplit("/", 1)[-1] for elem in results]
    return results 


def query_triplestore_byGenreAndPlatform(genreID, platformID):


    query = """PREFIX wd: <http://www.wikidata.org/entity/> 
    prefix : <http://www.example.org/semanticwebproject#>

    SELECT ?recGameID 
    WHERE {

    ?recGameID :onPlatform %s.
    ?recGameID :hasGenre %s.
    ?recGameID :hasPegi ?pegi

    FILTER (%d >= ?pegi)
    }
    """ % (
        platformID, 
        genreID,  
        userAge
        )
    results = get_results(endpoint_url, query)
    results = results['results']['bindings']
    results = [elem['recGameID']['value'] for elem in results]
    results = ["wd:" + elem.rsplit("/", 1)[-1] for elem in results]
    return results 



recommended_games_byGameAndAge = []


[ 
    recommended_games_byGameAndAge.extend(query_triplestore_byGameAndAge(gameID, userAge))
    for gameID in userGameIDs
]




recommended_games_byGenreAndPlatform = []
[
    [
    recommended_games_byGenreAndPlatform.extend(
        query_triplestore_byGenreAndPlatform(genreID, platformID)
        )  
        for platformID in userPlatformIDs
    ]
    for genreID in userGenreIDs
]

recommended_games_byGameAndAge = list(set(recommended_games_byGameAndAge)- set(recommended_games_byGenreAndPlatform))
recommended_games_byGenreAndPlatform = list(set(recommended_games_byGenreAndPlatform) - set(recommended_games_byGameAndAge))

random.shuffle(recommended_games_byGameAndAge)
recommended_games_byGameAndAge = recommended_games_byGameAndAge[:10]
random.shuffle(recommended_games_byGenreAndPlatform)
recommended_games_byGenreAndPlatform = recommended_games_byGenreAndPlatform[:10]


### getting the labels
recommended_games_byGameAndAge_labels = [
    gameLabels[gameID]
    for gameID in recommended_games_byGameAndAge
]
recommended_games_byGenreAndPlatform_labels = [
    gameLabels[gameID]
    for gameID in recommended_games_byGenreAndPlatform
]

### final message for the user 


sleep(1)
print("Based on your game history and your age, we recommend:\n")
print(*recommended_games_byGameAndAge_labels, sep = "\n")


sleep(2)
print("Based on your preferred genre and platform, we recommend:\n")
print(*recommended_games_byGenreAndPlatform_labels, sep = "\n")
sleep(1)