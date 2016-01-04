# coding=utf-8
from data.MongoDB import MongoDB
from data.TweetReader import TweetReader
from settings import twitter_config

mongodb = MongoDB()
reader = TweetReader(twitter_config)


def serialize_timeline_status(timeline_status):
    return {"lang": timeline_status.lang,
            "favorited": timeline_status.favorited,
            "truncated": timeline_status.truncated,
            "text": timeline_status.text,
            "created_at": timeline_status.created_at,
            "retweeted": timeline_status.retweeted,
            "source": timeline_status.source,
            "in_reply_to_screen_name": timeline_status.in_reply_to_screen_name,
            "id": timeline_status.id,
            "in_reply_to_user_id": timeline_status.in_reply_to_user_id
            }


print "starting process"
for status in reader.get_sample_stream_with_location():
    status["timeline"] = map(lambda t: serialize_timeline_status(t), reader.get_user_timeline(status['user']))
    mongodb.write(status)
