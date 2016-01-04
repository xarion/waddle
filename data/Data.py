from data.Filters import Filters
from data.MongoDB import MongoDB


class Data:
    def __init__(self, training_factor):
        self.mongodb = MongoDB()
        self.filters = Filters(self.mongodb)
        self.location_filter_query = self.filters.get_location_filter_query()
        self.doc_count = self.mongodb.tweets_collection.find({"$or": self.location_filter_query}).count()
        self.training_factor = training_factor
        self.training_doc_count = int(self.doc_count * self.training_factor)

    def get_training_data(self):
        return self.filters.filter_sources(
            self.mongodb.tweets_collection.find({"$or": self.location_filter_query}).limit(self.training_doc_count))

    def get_test_data(self):
        return self.filters.filter_sources(
            self.mongodb.tweets_collection.find({"$or": self.location_filter_query}).skip(self.training_doc_count))
