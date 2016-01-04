from helpers import Dictrement


class Filters:
    def __init__(self, mongodb):
        self.mongodb = mongodb
        self.source_whitelist = Filters.get_source_whitelist()

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

    @staticmethod
    def get_source_whitelist():
        whitelist = dict()
        with open("whitelist.txt") as file:
            for line in file.readlines():
                whitelist[line] = 1
        return whitelist

    @staticmethod
    def filter_timeline(timeline, whitelist):
        return filter(lambda status: status["source"] in whitelist, timeline)

    def filter_sources(self, docs):
        for doc in docs:
            doc["timeline"] = Filters.filter_timeline(doc["timeline"], self.source_whitelist)
            yield doc
