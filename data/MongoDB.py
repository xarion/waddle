# coding=utf-8
from pymongo import MongoClient

from settings import mongod_config


class MongoDB:
    tweets_collection_name = 'tweets'

    def __init__(self):
        self.client = MongoClient(mongod_config['connection_string'])
        self.db = self.client[mongod_config['database_name']]
        self.tweets_collection = self.db[MongoDB.tweets_collection_name]

    def write_stream(self, stream):
        for batch in stream:
            self.tweets_collection.insert_many(batch)

    def write(self, document):
        self.tweets_collection.insert_one(document)
