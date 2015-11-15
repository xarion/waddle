import ConfigParser

configParser = ConfigParser.RawConfigParser()
configParser.read('config')

config = dict()
config['consumer_key'] = configParser.get('twitter', 'consumer_key')
config['consumer_secret'] = configParser.get('twitter', 'consumer_secret')
config['access_token'] = configParser.get('twitter', 'access_token')
config['access_token_secret'] = configParser.get('twitter', 'access_token_secret')
