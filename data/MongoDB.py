# coding=utf-8
from pymongo import MongoClient

from settings import mongod_config


class MongoDB:
    tweets_collection_name = 'tweets'
    results_collection_name = 'results'
    def __init__(self):
        self.client = MongoClient(mongod_config['connection_string'])
        self.db = self.client[mongod_config['database_name']]
        self.tweets_collection = self.db[MongoDB.tweets_collection_name]
        self.results_collection = self.db[MongoDB.results_collection_name]

    def write_stream(self, stream):
        for batch in stream:
            self.tweets_collection.insert_many(batch)

    def write(self, document):
        self.tweets_collection.insert_one(document)

    def write_execution_result(self, result):
        self.results_collection.insert_one(result)
db = MongoDB()
