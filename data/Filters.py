import settings
from data.MongoDB import db


class Filters:
    def __init__(self):
        self.mongodb = db
        self.source_whitelist = Filters.get_source_whitelist()

    def get_location_filter_query(self):
        query = []
        for location_name in settings.locations.keys():
            query.append({"place.full_name": location_name})
        return query

    @staticmethod
    def get_source_whitelist():
        whitelist = dict()
        with open("config/whitelist.txt") as file:
            for line in file.read().splitlines():
                whitelist[line] = 1
        return whitelist

    def filter_tweets_by_sources(self, timeline):
        return filter(lambda status: status["source"] in self.source_whitelist, timeline)

    def filter_history_by_sources(self, docs):
        for doc in docs:
            doc["timeline"] = self.filter_tweets_by_sources(doc["timeline"])
            yield doc
