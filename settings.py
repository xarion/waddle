# coding=utf-8
import ConfigParser

configParser = ConfigParser.RawConfigParser()
configParser.read('config')

twitter_config = dict()
twitter_config['consumer_key'] = configParser.get('twitter', 'consumer_key')
twitter_config['consumer_secret'] = configParser.get('twitter', 'consumer_secret')
twitter_config['access_token'] = configParser.get('twitter', 'access_token')
twitter_config['access_token_secret'] = configParser.get('twitter', 'access_token_secret')

mongod_config = dict()
mongod_config['connection_string'] = configParser.get('mongod', 'connection_string')
mongod_config['database_name'] = configParser.get('mongod', 'database_name')
