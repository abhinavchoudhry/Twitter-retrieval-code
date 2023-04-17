import tweepy
import csv
from datetime import datetime, date, time, timedelta
import time
import pytz
import pandas as pd

# Add your Twitter API credentials here
consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''

# Authorization to consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Access to user's access key and access secret
auth.set_access_token(access_key, access_secret)

# Calling api
api = tweepy.API(auth, wait_on_rate_limit=True)

# keywords to search for
keywords = ['ai regulation', 'ai harm', 'ai risks', 'ai ethics', 'ai concerns']

# exclude retweets
query = ' OR '.join(keywords) + ' -filter:retweets'

# Date range to search for tweets in
start_date = datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
end_date = datetime(2023, 3, 29, 23, 59, 59, tzinfo=pytz.UTC)

# Open/create csv file to store data
csvFile = open('ai_regulation_tweets_april13.csv', 'a', newline='', encoding='utf-8')
csvWriter = csv.writer(csvFile)

# Cursor object to get tweets
tweets = tweepy.Cursor(api.search_tweets, q=query, tweet_mode='extended', lang='en', count=100).items()

# Loop through tweets and write to csv file
for tweet in tweets:
    try:
        # Skip retweets
        if tweet.full_text.startswith("RT"):
            continue

        tweet_date = tweet.created_at.replace(tzinfo=pytz.UTC)
        if tweet_date < end_date and tweet_date > start_date:
            csvWriter.writerow(
                [tweet.user.screen_name, tweet.full_text, tweet_date, tweet.user.location, tweet.entities['hashtags']])
    except tweepy.TweepError as e:
        print("Error : " + str(e))
        break
    except Exception as e:
        print("Error : " + str(e))
        continue

    # Wait for 15 minutes after every 15 requests
    if api.rate_limit_status()['resources']['search']['/search/tweets']['remaining'] == 0:
        reset_time = api.rate_limit_status()['resources']['search']['/search/tweets']['reset']
        time_to_wait = (reset_time - datetime.now(pytz.UTC)).total_seconds() + 5
        print(f"Rate limit reached. Waiting for {time_to_wait} seconds...")
        time.sleep(time_to_wait)

csvFile.close()

print("Tweets retrieved successfully!")