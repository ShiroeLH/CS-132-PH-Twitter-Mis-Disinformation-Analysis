from typing import ItemsView
import tweepy, csv, sys, re, openpyxl
import pandas as pd
import sched, time
import datetime

import config
import preprocess
import pprint

# Details
topic = "Red tagging students from state universities"
collector = "Rey Christian E. Delos Reyes"
keywords = [
    "(UPD OR PUP OR DLSU OR Ateneo)",
    "(Komunista OR NPA OR Elitista)"
]

# Open/create a file to append data to
csvFile = open('tweets/datasets/tweets_dataset_unfiltered.csv', 'a', newline='', encoding='utf-8')
csvWriter = csv.writer(csvFile)
csvWriter.writerow([
                    'TIMESTAMP', 'COLLECTOR', 'TOPIC', 'KEYWORDS', 'ACCOUNT HANDLE',
                    'ACCOUNT NAME', 'ACCOUNT BIO', 'JOINED', 'FOLLOWING', 'FOLLOWERS',
                    'LOCATION', 'RAW DATA', 'TRANSLATED DATA', 'DATE POSTED', 'TWEET URL',
                    'CONTENT TYPE', 'FAVORITES', 'REPLIES', 'RETWEETS',
                ])

# Authentication
auth = tweepy.OAuth2AppHandler(
    config.api_key, config.api_key_secret
)

# Get place ID
n           = 1000
api         = tweepy.API(auth)
places      = api.search_geo(query="Philippines", granularity="country"); place_id = places[0].id
query       = " AND ".join(keywords)  #+ " until:2023-01-01 since:2019-01-01" + " place:%s" % place_id
statuses    = api.search_tweets(q=query, count=n, tweet_mode="extended")
# tweets = tweepy.Cursor(api.search_tweets,q=query,until='2023-01-01',tweet_mode="extended").items(n)

for tweet in statuses:
    content_type = ', '.join(['text']+[entity for entity in tweet.entities.keys() if len(tweet.entities[entity])])

    csvWriter.writerow([
                    datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S %p"),                           # TIMESTAMP
                    collector,                                                                          # COLLECTOR
                    topic,                                                                              # TOPIC
                    keywords,                                                                           # KEYWORDS
                    '@' + tweet.user.screen_name,                                                       # ACCOUNT HANDLE
                    tweet.user.name,                                                                    # ACCOUNT NAME
                    tweet.user.description,                                                             # ACCOUNT BIO
                    tweet.user.created_at,                                                              # JOINED
                    tweet.user.friends_count,                                                           # FOLLOWING
                    tweet.user.followers_count,                                                         # FOLLOWERS
                    places[0].full_name,                                                                # LOCATION
                    tweet.full_text,                                                                    # RAW DATA
                    preprocess.simplify_text(tweet.full_text),                                          # TRANSLATED DATA
                    tweet.created_at,                                                                   # DATE POSTED
                    'https://twitter.com/' + tweet.user.screen_name + '/status/' + tweet.id_str,        # TWEET URL
                    content_type,                                                                       # CONTENT TYPE 
                    tweet.favorite_count,                                                               # FAVORITES 
                    tweet.in_reply_to_status_id_str,                                                    # REPLIES
                    tweet.retweet_count,                                                                # RETWEETS
                ])