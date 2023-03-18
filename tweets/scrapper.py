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
    "NPA",
    "PUP",
    "University of the Philippines",
    "(state university NPA)",
    "(UP AND NPA)",
    "(PUP AND NPA)",
    "(NPA AND breeding AND ground)",
    "terorista",
    "komunista",
    "CPP-NPA-NDF"
]

# # Open the dataset workbook
# workbook = openpyxl.load_workbook(filename = 'tweets/dataset.xlsx')
# # print(workbook.sheetnames)
# worksheet = workbook["Sample Data"]
# # print(worksheet.cell(row=2,column=1).value)

# Open/create a file to append data to
csvFile = open('tweets_dataset.csv', 'a', newline='', encoding='utf-8')

#Use csv writer
csvWriter = csv.writer(csvFile)

# Authentication
auth = tweepy.OAuth2AppHandler(
    config.api_key, config.api_key_secret
)

# Get place ID
api         = tweepy.API(auth)
places      = api.search_geo(query="Philippines", granularity="country"); place_id = places[0].id
#places     = api.search_geo(query="Manila", granularity="city"); place_id = places[1].id
query       = " OR ".join(keywords) + " place:%s" % place_id
n           = 1

print("(" + " OR ".join(keywords) +")" + " place:%s -is:retweet -has:media" % place_id)
print(place_id)

statuses = api.search_tweets(q=query, count=n, tweet_mode="extended")
# tweets = tweepy.Cursor(api.search_tweets,q=query,until='2023-01-01',tweet_mode="extended").items(n)

for tweet in statuses:
    print(tweet.full_text)
    
    content_type = ", ".join(["text"]+[entity for entity in tweet.entities.keys() if len(tweet.entities[entity])])

    csvWriter.writerow([
                    datetime.datetime.now(),#datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), PROBLEM WITH DATE TIME
                    collector,
                    topic,
                    ",".join(["\""+keyword+"\"" for keyword in keywords]),
                    "@" + tweet.user.screen_name,
                    tweet.user.name,
                    tweet.user.description,
                    "",
                    tweet.user.created_at,
                    tweet.user.friends_count,
                    tweet.user.followers_count,
                    places[0].full_name,
                    tweet.full_text,
                    preprocess.simplify_text(tweet.full_text),
                    "",
                    tweet.created_at,
                    "https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str,
                    content_type,
                    tweet.favorite_count,
                    tweet.in_reply_to_status_id_str,
                    tweet.retweet_count,
                    "",
                    "",
                    "",
                    "",
                    "",
                ])
        

# for tweet in tweets:
    # row = worksheet.max_row  + 1
    # worksheet.insert_rows(row)
    # print(row)

    # worksheet.cell(row=row, column=1).value = datetime.datetime.now()                                                       # TIMESTAMP         # datetime.datetime.now(),
    # worksheet.cell(row=row, column=2).value = collector                                                                     # COLLECTOR         # collector
    # worksheet.cell(row=row, column=3).value = topic                                                                         # TOPIC             # topic
    # worksheet.cell(row=row, column=4).value = ",".join(["\""+keyword+"\"" for keyword in keywords])                         # KEYWORDS          # ",".join(["\""+keyword+"\"" for keyword in keywords])
    # worksheet.cell(row=row, column=5).value = "@" + tweet.user.screen_name                                                  # ACCOUNT HANDLE    # "@" + tweet.user.screen_name
    # worksheet.cell(row=row, column=6).value = tweet.user.name                                                               # ACCOUNT NAME      # tweet.user.name
    # worksheet.cell(row=row, column=7).value = tweet.user.description                                                        # ACCOUNT BIO       # tweet.user.description
    # # ACCOUNT TYPE      # 
    # worksheet.cell(row=row, column=9).value = tweet.user.created_at                                                         # JOINED            # tweet.user.created_at
    # worksheet.cell(row=row, column=10).value = tweet.user.friends_count                                                     # FOLLOWING         # tweet.user.friends_count
    # worksheet.cell(row=row, column=11).value = tweet.user.followers_count                                                   # FOLLOWERS         # tweet.user.followers_count
    # worksheet.cell(row=row, column=12).value = places[0].full_name                                                          # LOCATION          # places[0].full_name
    # worksheet.cell(row=row, column=13).value = tweet.full_text                                                              # RAW DATA          # tweet.full_text
    # worksheet.cell(row=row, column=14).value = preprocess.simplify_text(tweet.full_text)                                    # TRANSLATED DATA   # preprocess.simplify_text(tweet.full_text)
    # # DATA TYPE         # 
    # worksheet.cell(row=row, column=16).value = tweet.created_at                                                             # DATE POSTED       # tweet.created_at
    # worksheet.cell(row=row, column=17).value = "https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str  # TWEET URL         # "https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str
    # # SCREENSHOT        # 
    # worksheet.cell(row=row, column=18).value = content_type                                                                 # CONTENT TYPE      # ", ".join(["text"]+[entity for entity in tweet.entities.keys() if len(tweet.entities[entity])])
    # worksheet.cell(row=row, column=19).value = tweet.favorite_count                                                         # FAVORITES         # tweet.favorite_count
    # worksheet.cell(row=row, column=20).value = tweet.in_reply_to_status_id_str                                              # REPLIES           # tweet.in_reply_to_status_id_str
    # worksheet.cell(row=row, column=21).value = tweet.retweet_count                                                          # RETWEETS          # tweet.retweet_count
    # # QOUTE TWEETS      # 
    # # VIEWS             # 
    # # RATING            # 
    # # REASONING         # 
    # # OTHER DATA        #