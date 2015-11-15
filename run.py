from data import MongoDB
from reader import TweetReader
from settings import twitter_config, mongod_config

mongodb = MongoDB(mongod_config)
reader = TweetReader(twitter_config)

mongodb.write_stream(reader.get_sample_stream_with_location())
