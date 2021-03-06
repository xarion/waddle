# coding=utf-8
import ConfigParser

configParser = ConfigParser.RawConfigParser()
configParser.read('config/config.conf')

twitter_config = dict()
twitter_config['consumer_key'] = configParser.get('twitter', 'consumer_key')
twitter_config['consumer_secret'] = configParser.get('twitter', 'consumer_secret')
twitter_config['access_token'] = configParser.get('twitter', 'access_token')
twitter_config['access_token_secret'] = configParser.get('twitter', 'access_token_secret')

mongod_config = dict()
mongod_config['connection_string'] = configParser.get('mongod', 'connection_string')
mongod_config['database_name'] = configParser.get('mongod', 'database_name')

streaming_config = dict()
streaming_config['chunk_size'] = int(configParser.get('streaming', 'chunk_size'))
streaming_config['total_chunks'] = int(configParser.get('streaming', 'total_chunks'))

locations = {"Manhattan, NY": 1,
             "Los Angeles, CA": 2,
             "Houston, TX": 3,
             "Chicago, IL": 4,
             "San Francisco, CA": 5,
             "Philadelphia, PA": 6,
             "Washington, DC": 7,
             "Atlanta, GA": 8}
