from reader import TweetReader

reader = TweetReader()
for sample in reader.get_tweet_samples_with_location():
    print sample
