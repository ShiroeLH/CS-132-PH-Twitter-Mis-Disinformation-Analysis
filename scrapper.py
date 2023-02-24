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
    "UP",
    "NPA",
    "PUP",
    "state university NPA",
    "UP NPA",
    "PUP NPA",
    "NPA breeding ground",
    "terorista",
    "komunista",
    "CPP-NPA-NDF"
]

# Open the dataset workbook
workbook = openpyxl.load_workbook(filename = 'dataset.xlsx')
worksheet = workbook["Sample Data"]

# Authentication
auth = tweepy.OAuth2AppHandler(
    config.api_key, config.api_key_secret
)

# Get place ID
api         = tweepy.API(auth)
places      = api.search_geo(query="Philippines", granularity="country"); place_id = places[0].id
#places     = api.search_geo(query="Manila", granularity="city"); place_id = places[1].id
query       = "place:%s -is:retweet -has:media" % place_id #print(" OR ".join(keywords))
n           = 1


#statuses = api.search_tweets(q=query, count=10000)
tweets = tweepy.Cursor(api.search_tweets,q=query,tweet_mode="extended").items(n)

for tweet in tweets:
    content_type = [entity for entity in tweet.entities.keys if len(tweet.entities[entity])]
    if tweet.full_text: content_type.append("text")
    # TIMESTAMP         # datetime.datetime.now(),
    # COLLECTOR         # collector
    # TOPIC             # topic
    # KEYWORDS          # ",".join(["\""+keyword+"\"" for keyword in keywords])
    # ACCOUNT HANDLE    # "@" + tweet.user.screen_name
    # ACCOUNT NAME      # tweet.user.name
    # ACCOUNT BIO       # tweet.user.description
    # ACCOUNT TYPE      # 
    # JOINED            # tweet.user.created_at
    # FOLLOWING         # tweet.user.friends_count
    # FOLLOWERS         # tweet.user.followers_count
    # LOCATION          # places[0].full_name
    # RAW DATA          # tweet.full_text
    # TRANSLATED DATA   # preprocess.simplify_text(tweet.full_text)
    # DATA TYPE         # 
    # DATE POSTED       # tweet.created_at
    # TWEET URL         # "https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str
    # SCREENSHOT        # 
    # CONTENT TYPE      # ", ".join(["text"]+[entity if len(tweet.entities[entity]) for entity in tweet.entities.keys])
    # FAVORITES         # 
    # REPLIES           # 
    # RETWEETS          # 
    # QOUTE TWEETS      # 
    # VIEWS             # 
    # RATING            # 
    # REASONING         # 
    # OTHER DATA        # 

    print(tweet)
    print("https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str)
    print(content_type)
    # print(tweet.full_text)
    # print(preprocess.re_punc(tweet.full_text))
    # print(preprocess.re_emoji(tweet.full_text))
    # print(preprocess.simplify_text(tweet.full_text))
    
    # if preprocess.simplify_text(tweet.full_text):
    #     csvWriter.writerow([    
    #         datetime.datetime.now(),
    #         collector,
    #         topic,
    #         ",".join(["\""+keyword+"\"" for keyword in keywords]),
    #         tweet.full_text.encode('utf-8'),
    #         preprocess.simplify_text(tweet.full_text),
    #     ])