# coding=utf-8
import twitter

from helpers import ChunkedStream


class TweetReader:
    def __init__(self, twitter_config):
        self.api = twitter.Api(consumer_key=twitter_config['consumer_key'],
                               consumer_secret=twitter_config['consumer_secret'],
                               access_token_key=twitter_config['access_token'],
                               access_token_secret=twitter_config['access_token_secret'])

    def get_sample_stream(self):
        return self.api.GetStreamSample()

    # Training Data
    @ChunkedStream()
    def get_sample_stream_with_location(self):  # training data
        stream = self.get_sample_stream()
        for sample in stream:
            if 'contributors' in sample:  # this is a tweet
                if sample['geo'] is not None \
                        and sample['geo']['type'] is u"Point" \
                        and sample['place']['country_code'] is "US"\
                        and sample['lang'] is "en":
                    print("yielding")
                    yield sample

    def get_user_timeline(self, user):
        return self.api.GetUserTimeline(user_id=user["id"], exclude_replies=True, count=40)
