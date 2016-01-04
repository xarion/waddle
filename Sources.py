from data import MongoDB
from helpers import Dictrement
from settings import mongod_config

mongodb = MongoDB(mongod_config)
docs = mongodb.tweets_collection.find()
source_dictrement = Dictrement()

for doc in docs:
    for status in doc['timeline']:
        source = status["source"]
        source_dictrement.increment(source)

print source_dictrement.get_dict()
