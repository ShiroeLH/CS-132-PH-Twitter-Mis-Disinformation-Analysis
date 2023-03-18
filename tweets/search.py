from typing import ItemsView
import tweepy, csv, sys, re, openpyxl
import pandas as pd
import sched, time
import datetime

import config
import preprocess
import pprint

# Open the dataset workbook
workbook = openpyxl.load_workbook(filename = 'tweets/datasets/Dataset - Group 32 datasheet.xlsx')
worksheet = workbook['Data']

# Collect status IDs
statuses = []
for iterator in range(3,worksheet.max_row):
    statuses.append(worksheet.cell(row=iterator,column=3).value)
status_ids = [int(status.split('/')[-1]) for status in statuses]

# Open/create a file to append data to and use csv writer
csvFile = open('tweets/datasets/tweets_dataset.csv', 'a', newline='', encoding='utf-8')
csvWriter = csv.writer(csvFile)

# Authentication
auth = tweepy.OAuth2AppHandler(
    config.api_key, config.api_key_secret
)
api  = tweepy.API(auth)

# Prelimenary data
topic       = 'Red tagging students from state universities'
collector   = 'Rey Christian E. Delos Reyes'
keywords    = '(UPD OR PUP OR DLSU OR Ateneo) AND (Komunista OR NPA OR Elitista) until:2023-01-01 since:2019-01-01'
places      = api.search_geo(query="Philippines", granularity="country"); place_id = places[0].id

# Get all statuses
for id in status_ids:
    tweet = api.get_status(id, tweet_mode='extended')
    content_type = ', '.join(['text']+[entity for entity in tweet.entities.keys() if len(tweet.entities[entity])])

    csvWriter.writerow([
                    datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S %p"),
                    collector,
                    topic,
                    keywords,
                    '@' + tweet.user.screen_name,
                    tweet.user.name,
                    tweet.user.description,
                    '',
                    tweet.user.created_at,
                    tweet.user.friends_count,
                    tweet.user.followers_count,
                    places[0].full_name,
                    tweet.full_text,
                    preprocess.simplify_text(tweet.full_text),
                    '',
                    tweet.created_at,
                    'https://twitter.com/' + tweet.user.screen_name + '/status/' + tweet.id_str,
                    content_type,
                    tweet.favorite_count,
                    tweet.in_reply_to_status_id_str,
                    tweet.retweet_count,
                    '',
                    '',
                    '',
                    '',
                    '',
                ])
