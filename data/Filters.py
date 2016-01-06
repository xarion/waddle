import settings


class Filters:
    def __init__(self, mongodb):
        self.mongodb = mongodb
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
