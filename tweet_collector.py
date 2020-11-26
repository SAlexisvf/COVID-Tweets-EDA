import os
import tweepy as tw
import pandas as pd
import datetime
import random
import ast
import argparse
from credentials import *

def tweet_collector(date, max_tweets):
    auth = tw.OAuthHandler(consumer_api_key, consumer_api_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth)

    with open('covid_tweets_id/covid_' + date + '.txt') as f:
        lines = f.readlines()
    data = [ast.literal_eval(line) for line in lines]

    tweets_df = pd.DataFrame()
    miss_count, retrieved_count = (0,0)
    while retrieved_count < max_tweets:
        # pick a tweet ID randomly
        random_id = random.choice(data[0])
        try:
            tweet = api.get_status(random_id)    
        except:
            miss_count = miss_count + 1
            print('missed tweets: ' + str(miss_count))
            data[0].remove(random_id)
        else:
            hashtags = []
            for hashtag in tweet.entities["hashtags"]:
                hashtags.append(hashtag["text"])
            # appends to dataframe
            tweets_df = tweets_df.append(pd.DataFrame({'user_location': tweet.user.location,\
                                                    'user_followers': tweet.user.followers_count,
                                                    'retweet_count': tweet.retweet_count,
                                                    'favorite_count': tweet.favorite_count,
                                                    'user_verified': tweet.user.verified,
                                                    'date': tweet.created_at,
                                                    'text': tweet.text, 
                                                    'hashtags': [hashtags if hashtags else None],
                                                    'source': tweet.source,}, index=[0]))

            data[0].remove(random_id)
            retrieved_count = retrieved_count + 1
            print('tweets retrieved: ' + str(retrieved_count))

    tweets_df.to_csv(date + '.csv', index=False)
    print('Tweets dataframe succesfully loaded and saved as: ' + date + '.csv')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tweet collector")
    parser.add_argument('-d', '--date', type=str, required=True, help='Date (YYYY_MM_DD)')
    parser.add_argument('-c', '--count', type=int, required=True, help='Maximun tweets to be collected')
    args = parser.parse_args()
    tweet_collector(args.date, args.count)