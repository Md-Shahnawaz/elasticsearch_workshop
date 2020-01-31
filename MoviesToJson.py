import csv
import re
from collections import deque
import elasticsearch
from elasticsearch import helpers

csvfile = open('/Users/1022590/Shahnawaz/Personal/elasticsearch/ml-latest-small/movies.csv', 'r')

reader = csv.DictReader( csvfile )
def movies():
    for movie in reader:
        movie_dict = {}
        title = re.sub(" \(.*\)$", "", re.sub('"','', movie['title']))
        year = movie['title'][-5:-1]
        if (not year.isdigit()):
            year = "2016"
        genres = movie['genres'].split('|')
        movie_dict["id"] = movie["movieId"]
        movie_dict["title"] = title
        movie_dict["year"] = year
        movie_dict["genre"] = genres
        yield movie_dict

es = elasticsearch.Elasticsearch()
es.indices.delete(index="movies", ignore=404)
es.indices.create(index='movies', body={
   'settings' : {
         'index' : {
              'number_of_shards':1 ,
              'number_of_replicas':1
         }
   }
})
deque(helpers.parallel_bulk(es, movies(), index="movies", doc_type="doc"), maxlen=0)
es.indices.refresh()