import operator

from data.MongoDB import db
from helpers import Dictrement

mongo = db

docs = mongo.tweets_collection.find({}, {"place.full_name": 1, "_id": 0})
location_counts = Dictrement()
count = 0
for doc in docs:
    location_fullname = doc['place']['full_name']
    location_counts.increment(location_fullname)
    count += 1

results = sorted(location_counts.get_dict().items(), key=operator.itemgetter(1))
for result in reversed(results[-10:]):
    print "%s: %d" % (result[0], result[1])

print count