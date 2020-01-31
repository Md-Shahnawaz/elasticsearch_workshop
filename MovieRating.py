import csv
import re
from collections import deque
import elasticsearch
from elasticsearch import helpers

def movies_title_lookup():

    csvfile = open('/Users/1022590/Shahnawaz/Personal/elasticsearch/ml-latest-small/movies.csv', 'r')
    reader = csv.DictReader(csvfile)
    movie_dict = {}
    for movie in reader:
        movie_dict[movie["movieId"]] = movie["title"]
    return movie_dict

def readRating():

    csvfile = open('/Users/1022590/Shahnawaz/Personal/elasticsearch/ml-latest-small/ratings.csv', 'r')
    reader = csv.DictReader(csvfile)
    titleLookup = movies_title_lookup()

    for line in reader:
        rating = {}
        rating['user_id'] = int(line['userId'])
        rating['movie_id'] = int(line['movieId'])
        rating['title'] = titleLookup[line['movieId']]
        rating['rating'] = float(line['rating'])
        rating['timestamp'] = float(line['timestamp'])
        yield rating


es = elasticsearch.Elasticsearch()
es.indices.delete(index="ratings", ignore=404)
deque(helpers.parallel_bulk(es, readRating(), index="ratings", doc_type="doc"), maxlen=0)
es.indices.refresh()

