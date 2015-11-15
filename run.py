from reader import TweetReader
from settings import twitter_config

reader = TweetReader(twitter_config)

for sample in reader.get_tweet_samples_with_location():
    print sample
