# coding=utf-8
from pymongo import MongoClient


class MongoDB:
    tweets_collection = 'tweets'

    def __init__(self, mongodb_config):
        self.client = MongoClient(mongodb_config['connection_string'])
        self.db = self.client[mongodb_config['database_name']]
        self.tweets_collection = self.db[MongoDB.tweets_collection]

    def write_stream(self, stream):
        for batch in stream:
            self.tweets_collection.insert_many(batch)
