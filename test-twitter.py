import tweepy
import sys
import os
import json
from types import SimpleNamespace
from configparser import ConfigParser

twitter_accs = ['@obillustrations', '@cma_drawings']

def get_twitter_keys(filename: str) -> str:
    config = ConfigParser()
    config.read('apikey.txt')
    api_key = config.get('auth', 'api_key')
    api_secret = config.get('auth', 'api_secret')
    access_token = config.get('auth', 'access_token')
    access_token_secret = config.get('auth', 'access_token_secret')

    return api_key, api_secret, access_token, access_token_secret

key, secret, access_token, access_token_secret = get_twitter_keys('apikey.txt')
auth = tweepy.OAuthHandler(key, secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

result_set = api.user_timeline(screen_name=twitter_accs, count=1, exclude_replies=True, include_rts=False, tweet_mode="extended")
status = result_set[0]
json_str = json.dumps(status._json)
post_object = json.loads(json_str, object_hook=lambda d: SimpleNamespace(**d))
print(post_object.entities.media[0].media_url)