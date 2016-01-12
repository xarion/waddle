from data.Filters import Filters
from data.MongoDB import db


class Data:
    def __init__(self, training_factor=0.5, include_user_history=True):
        self.mongodb = db
        self.training_factor = training_factor
        self.filters = Filters()
        self.location_filter_query = self.filters.get_location_filter_query()
        self.doc_count = self.__get_cursor__().count()
        self.training_doc_count = int(self.doc_count * self.training_factor)
        self.include_user_history = include_user_history

    def get_training_data(self):
        if self.include_user_history:
            return self.filters.filter_history_by_sources(
                    self.__get_cursor__().limit(self.training_doc_count))
        else:
            return self.filters.filter_tweets_by_sources(
                    self.__get_cursor__().limit(self.training_doc_count))

    def get_test_data(self):
        if self.include_user_history:
            return self.filters.filter_history_by_sources(
                    self.__get_cursor__().skip(self.training_doc_count))
        else:
            return self.filters.filter_tweets_by_sources(
                    self.__get_cursor__().skip(self.training_doc_count))

    def __get_cursor__(self):
        return self.mongodb.tweets_collection.find({"$or": self.location_filter_query})
