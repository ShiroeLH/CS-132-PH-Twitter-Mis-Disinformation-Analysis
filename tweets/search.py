from typing import ItemsView
import tweepy, csv, sys, re, openpyxl
import pandas as pd
import sched, time
import datetime
import xlsxwriter

import config
import preprocess
import pprint

# Open the dataset workbook
workbook = openpyxl.load_workbook(filename = 'tweets/datasets/Dataset - Group 32 datasheet.xlsx')
worksheet = workbook['Data']

# Write to another workbook
workbook2 = xlsxwriter.Workbook('tweets/datasets/tweets_dataset.xlsx')
worksheet2 = workbook2.add_worksheet()

# Collect status IDs
statuses = []
for iterator in range(3,worksheet.max_row):
    statuses.append(worksheet.cell(row=iterator,column=3).value)
status_ids = [int(status.split('/')[-1]) for status in statuses]

# Open/create a file to append data to and use csv writer
csvFile = open('tweets/datasets/tweets_dataset.csv', 'a', newline='', encoding='utf-8')
csvWriter = csv.writer(csvFile)
# csvWriter.writerow([
#                     'TIMESTAMP', 'COLLECTOR', 'TOPIC', 'KEYWORDS', 'ACCOUNT HANDLE',
#                     'ACCOUNT NAME', 'ACCOUNT BIO', 'JOINED', 'FOLLOWING', 'FOLLOWERS',
#                     'LOCATION', 'RAW DATA', 'TRANSLATED DATA', 'DATE POSTED', 'TWEET URL',
#                     'CONTENT TYPE', 'FAVORITES', 'RETWEETS',
#                 ])

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

# Write preliminary data
headers = [
    'TIMESTAMP', 'COLLECTOR', 'TOPIC', 'KEYWORDS', 'ACCOUNT HANDLE',
    'ACCOUNT NAME', 'ACCOUNT BIO', 'JOINED', 'FOLLOWING', 'FOLLOWERS',
    'LOCATION', 'RAW DATA', 'TRANSLATED DATA', 'DATE POSTED', 'TWEET URL',
    'CONTENT TYPE', 'FAVORITES', 'RETWEETS',
]

for index, id in enumerate(headers):
    worksheet2.write(0, index, id)

# Get all statuses
for index, id in enumerate(status_ids):
    tweet = api.get_status(id, tweet_mode='extended')
    content_type = ', '.join(['text']+[entity for entity in tweet.entities.keys() if len(tweet.entities[entity])])

    worksheet2.write(index+1, 0, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S %p"))
    worksheet2.write(index+1, 1, collector)
    worksheet2.write(index+1, 2, topic)
    worksheet2.write(index+1, 3, keywords)
    worksheet2.write(index+1, 4, '@' + tweet.user.screen_name)
    worksheet2.write(index+1, 5, tweet.user.name)
    worksheet2.write(index+1, 6, tweet.user.description)
    worksheet2.write(index+1, 7, tweet.user.created_at.strftime("%d/%m/%Y %H:%M:%S %p"))
    worksheet2.write(index+1, 8, tweet.user.friends_count)
    worksheet2.write(index+1, 9, tweet.user.followers_count)
    worksheet2.write(index+1, 10, places[0].full_name)
    worksheet2.write(index+1, 11, tweet.full_text)
    worksheet2.write(index+1, 12, preprocess.simplify_text(tweet.full_text))
    worksheet2.write(index+1, 13, tweet.created_at.strftime("%d/%m/%Y %H:%M:%S %p"))
    worksheet2.write(index+1, 14, 'https://twitter.com/' + tweet.user.screen_name + '/status/' + tweet.id_str)
    worksheet2.write(index+1, 15, content_type)
    worksheet2.write(index+1, 16, tweet.favorite_count)
    # worksheet2.write(index+1, 17, tweet.in_reply_to_status_id_str)
    worksheet2.write(index+1, 17, tweet.retweet_count)


workbook2.close()