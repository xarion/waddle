## count tweet sources
import operator

from data.MongoDB import db
from helpers import Dictrement

mongodb = db
docs = mongodb.tweets_collection.find()
source_dictrement = Dictrement()
count = 0
for doc in docs:
    for status in doc['timeline']:
        source = status["source"]
        source_dictrement.increment(source)
        count += 1

filter_at = float(count) * 0.001
results = sorted(source_dictrement.get_dict().items(), key=operator.itemgetter(1))
for result in reversed(results):
    if result[1] > filter_at:
        print "%s: %d" % (result[0], result[1])
    else:
        break
