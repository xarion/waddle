# coding=utf-8
from pymongo import MongoClient

from helpers import Dictrement


class MongoDB:
    tweets_collection_name = 'tweets'

    def __init__(self, mongodb_config):
        self.client = MongoClient(mongodb_config['connection_string'])
        self.db = self.client[mongodb_config['database_name']]
        self.tweets_collection = self.db[MongoDB.tweets_collection_name]

    def write_stream(self, stream):
        for batch in stream:
            self.tweets_collection.insert_many(batch)

    def write(self, document):
        self.tweets_collection.insert_one(document)


class Data:
    def __init__(self, mongodb):
        self.mongodb = mongodb

    def get_filtered_locations(self):
        docs = self.mongodb.tweets_collection.find({}, {"place.full_name": 1, "_id": 0})
        location_counts = Dictrement()
        count = 0
        for doc in docs:
            location_fullname = doc['place']['full_name']
            location_counts.increment(location_fullname)
            count += 1

        filtered_locations = location_counts.get_dict()
        for n in filtered_locations.keys():
            if filtered_locations[n] < count * 0.01:
                del filtered_locations[n]

        return filtered_locations

    def get_location_filter_query(self):
        query = []
        for location_name in self.get_filtered_locations().keys():
            query.append({"place.full_name": location_name})
        return query

    def get_training_data(self):
        pass
