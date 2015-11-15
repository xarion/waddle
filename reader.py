import twitter


class TweetReader:
    def __init__(self, twitter_config):
        self.api = twitter.Api(consumer_key=twitter_config['consumer_key'],
                               consumer_secret=twitter_config['consumer_secret'],
                               access_token_key=twitter_config['access_token'],
                               access_token_secret=twitter_config['access_token_secret'])

    def get_tweet_samples_with_location(self):
        samples = self.api.GetStreamSample()

        for sample in samples:
            if 'contributors' in sample:  # this is a tweet
                if sample['geo'] is not None and sample['geo']['type'] == u"Point":
                    yield sample
