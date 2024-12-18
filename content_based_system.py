import pandas as pd
import pickle
import sqlite3
import webbrowser
import os

# File paths
project_folder = os.getcwd()
DATA_FOLDER = project_folder+'/Data/'

anime = pd.read_pickle(DATA_FOLDER+'anime')
anime_features = pd.read_pickle(DATA_FOLDER+'anime_features')
filename = DATA_FOLDER+'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))
distances, indices = loaded_model



def get_ID(name):
    with sqlite3.connect(DATA_FOLDER+"animeData.db") as  db: #anime database
            c = db.cursor()
            findID=("SELECT anime_id from t WHERE name=?")
            c.execute(findID,[name])
            
            results = c.fetchall()
            db.commit()
    return results


all_anime_names = list(anime.name.values)

idSearch = []

def get_possible_searches(partial):
    possibleSearch=[]
    for name in all_anime_names:
        if partial in name:
            possibleSearch.append(name)
    return possibleSearch

def get_index_from_name(name):
    return anime[anime["name"]==name].index.tolist()[0]

def get_similar_animes(query=None,id=None):
    rec=[]
    if id:
        for id in indices[id][1:]:
            print(anime.ix[id]["name"])
    if query:
        found_id = get_index_from_name(query)
        for id in indices[found_id][1:]:
            rec.append((anime.ix[id]["name"]))
    return rec


