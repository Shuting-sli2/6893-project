#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing all dependencies
import numpy as np
import tweepy
import requests
import base64
import csv
import json
import time
def Get_Trends(consumer_key, consumer_secret):
    # Import the Google Cloud client library and JSON library
    #from google.cloud import storage

    #Define your keys from the developer portal
    #consumer_key = 'YwjSpr3oPZjPg2mDxghAJ4ing'
    #consumer_secret = 'SN0Jb3iwE93eN0BoJSRWkWptPXI628ECA5ce1Yapeg81SoY6Up'

    #Reformat the keys and encode them
    key_secret = '{}:{}'.format(consumer_key, consumer_secret).encode('ascii')
    #Transform from bytes to bytes that can be printed
    b64_encoded_key = base64.b64encode(key_secret)
    #Transform from bytes back into Unicode
    b64_encoded_key = b64_encoded_key.decode('ascii')

    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)
    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    auth_data = {
        'grant_type': 'client_credentials'
    }
    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    #print(auth_resp.status_code)
    access_token = auth_resp.json()['access_token']

    # If the status code printed is 200 then the request worked successfully.

    trend_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    # id:  "where on earth identifier" or WOEID
    # 1: the global information
    trend_params = {
        'id': 1,
    }

    trend_url = 'https://api.twitter.com/1.1/trends/place.json'

    if True:
        trend_resp = requests.get(trend_url, headers=trend_headers, params = trend_params)
        # get response in JSON
        tweet_data = trend_resp.json()
        #print(tweet_data[0]['trends'])
        # The response contains the trending topics tweets and its various parameters in JSON format.

        # print the top trending tweets
        # name: name of the trending topics, sometimes include hashtag

        # top 50
        output_data = {"trending_tweets":[]}

        def add_tweet(tweet):
            output_data["trending_tweets"].append(tweet)

        for i in range(0,50):
            tweet = {}
            tweet["name"] = tweet_data[0]['trends'][i]['name']
            tweet["tweet_volume"] = tweet_data[0]['trends'][i]['tweet_volume']
            add_tweet(tweet)
          #to_csv.append(tweet_data[0]['trends'][i])
          #print(tweet_data[0]['trends'][i])
          #save tweet content to a csv
          #twtname = tweet_data[0]['trends'][i]['name']

        #json_output = json.dumps(output_data["trending_tweets"], indent=2)
        #print(json_output)
        #storage_client = storage.Client()
        #bucket = storage_client.get_bucket('twitter1000')
        #blob = bucket.get_blob("trend.json")
        #blob.upload_from_string(json_output)
        #print("pause for 60 second")
        with open("trend.json", "w") as f:
                json.dump(output_data["trending_tweets"], f, indent = 2)
        #read json from gcp
        '''
        data = json.loads(blob.download_as_string())
        print data
        '''

        #time.sleep(60)


# In[ ]:




