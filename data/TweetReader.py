# coding=utf-8
import twitter


class TweetReader:
    def __init__(self, twitter_config):

        self.api = twitter.Api(consumer_key=twitter_config['consumer_key'],
                               consumer_secret=twitter_config['consumer_secret'],
                               access_token_key=twitter_config['access_token'],
                               access_token_secret=twitter_config['access_token_secret'])

    def get_sample_stream(self):
        return self.api.GetStreamSample()

    # Training Data
    # @ChunkedStream()
    def get_sample_stream_with_location(self):  # training data
        for sample in self.get_sample_stream():
            if TweetReader.filter(sample):
                yield sample

    def get_user_timeline(self, user):
        return self.api.GetUserTimeline(user_id=user["id"], exclude_replies=True, count=40)

    @staticmethod
    def filter(sample):
        return 'contributors' in sample and \
               sample['geo'] is not None \
               and sample['lang'] == u"en" \
               and sample['geo']['type'] == u"Point" \
               and sample['place']['country_code'] == u"US"
