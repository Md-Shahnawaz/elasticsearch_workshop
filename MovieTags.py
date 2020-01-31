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

def get_tags():

    csvfile = open('/Users/1022590/Shahnawaz/Personal/elasticsearch/ml-latest-small/tags.csv', 'r')
    reader = csv.DictReader(csvfile)
    titleLookup = movies_title_lookup()

    for line in reader:
        tags = {}
        tags['user_id'] = int(line['userId'])
        tags['movie_id'] = int(line['movieId'])
        tags['title'] = titleLookup[line['movieId']]
        tags['tag'] = line['tag']
        tags['timestamp'] = float(line['timestamp'])
        yield tags


es = elasticsearch.Elasticsearch()
es.indices.delete(index="tags", ignore=404)
deque(helpers.parallel_bulk(es, get_tags(), index="tags", doc_type="doc"), maxlen=0)
es.indices.refresh()