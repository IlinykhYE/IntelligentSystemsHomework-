import io
from surprise import KNNWithMeans
from surprise import Dataset
from surprise import get_dataset_dir
from collections import defaultdict
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import re

from SPARQLWrapper import SPARQLWrapper, JSON
from sys import argv


def read_names():
    file_name = get_dataset_dir() + '/ml-100k/ml-100k/u.item'
    rid_to_name = {}
    with io.open(file_name, 'r', encoding='ISO-8859-1') as f:
        for line in f:
            line = line.split('|')
            rid_to_name[line[0]] = (line[1], line[2])
    return rid_to_name


def get_top_n(predictions, n=5):
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, round(est, 3)))
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]
    return top_n

user_id = input('User id: ')

data = Dataset.load_builtin('ml-100k')
trainset = data.build_full_trainset()
sim_options = {'name': 'cosine', 'user_based': True, 'min_support': 5}
algo = KNNWithMeans(k=4, sim_options=sim_options)
algo.fit(trainset)
testset = trainset.build_anti_testset()
testset = filter(lambda x: x[0] == user_id, testset)
predictions = algo.test(testset)

top_n = get_top_n(predictions)
rid_to_name = read_names()
print('User ' + user_id)

item_map = read_names()
name_films=[]
for movie_rid, rating in top_n[user_id]:
    name_films.append(item_map[movie_rid][0])
    print('{:4s} {:<60s} {}'.format(movie_rid, str(rid_to_name[movie_rid]), rating))

    #добиваемся правильного написания названия фильма
for k,_ in enumerate(name_films):
    name_films[k]=name_films[k][:-6]
    if(',' in name_films[k]):
        temp=name_films[k].split(',')
        name_films[k]=temp[1]+temp[0]
    name_films[k]=name_films[k].strip()

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

query = """
SELECT ?filmLabel ?studioLabel WHERE {
  BIND("%s"@en AS ?la)
     ?f wdt:P31 wd:Q11424;
     rdfs:label ?la;
     wdt:P915 ?studio.
  ?studio wdt:P31 wd:Q375336.
  ?film wdt:P915 ?studio.
  ?film wdt:P31 wd:Q11424.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
} LIMIT 10
"""
for film in name_films:
    print("Запрос для фильма: "+film)
    print(query % film)
    sparql.setQuery(query % film)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        film = result['filmLabel']['value']
        studio = result['studioLabel']['value']
        print("{}  -  {}".format(film ,studio))
    print()
