import json
from pprint import pprint
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

class MyElasticsearch():
    def __init__(self, data, schema):
        self.es = Elasticsearch()
        self.data = data
        self.schema = schema

    def create_news_index(self):
        if not self.es.indices.exists("es_news"):
            news_index = self.es.indices.create(index = "es_news", body = self.schema)

    def format_action(self, id, value):
        return {
            "_index": "es_news",
            "_type": "news",
            "_id": id,
            "_source": value
        }

    def bulk_insert(self):
        actions = []
        for key, value in self.data.iteritems():
            #change value
            actions.append(self.format_action(key, value))
        helpers.bulk(self.es, actions, stats_only=True)

    def q_category(self, field_name, value):
        query_body={
            "query":{
                "match":{
                    field_name: value
                }
            }
        }
        res = self.es.search(index="es_news", doc_type="news", body=query_body)
        return res['hits']['hits']

    def q_keywords(self, value):
        query_body={
            "query":{
                "multi_match":{
                    "query": value,
                    "fields": ["section^1", "title^3", "abstract^2", "content^2", "byline^1", "source^1", "des_facet^1", "geo_facet^1"]
                }
            }
        }
        res = self.es.search(index="es_news", doc_type="news", body=query_body)
        return res['hits']['hits']

with open("health2.json") as data_file:
    data = json.load(data_file)
with open("es_mapping_file.json") as data_file2:
    schema = json.load(data_file2)
myElasticsearch = MyElasticsearch(data, schema)
myElasticsearch.create_news_index()
myElasticsearch.bulk_insert()
rs = myElasticsearch.es.search(index="es_news", body={"query":{"match_all":{}})
print rs['hits']['total']
