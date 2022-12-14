#importing all dependencies
import numpy as np
import tweepy
import requests
import base64
import csv
import json

#Define your keys from the developer portal
consumer_key = '47woRli9HY5DaaQOJyV3xC3Dn'
consumer_secret = 'Ol4k0MbQM7zyL4suBn09y7SRYFAMjSom7nb11PNEew3uQhmEMZ'

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

json_output = json.dumps(output_data["trending_tweets"], indent=2)

print(json_output)
with open("/Users/shutingli/Desktop/6893_project/trend.json", "w") as outfile:
    outfile.write(json_output)

# while streaming, calling the getTrend api at every second
# continue for ex. 60 seconds
# store analysis in a dataset
'''
keys = to_csv[0].keys()
with open('/Users/shutingli/Desktop/trend.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(to_csv)
'''
#NMA2022
#YalıÇapkını
#NRJMusicAwards
#RLWC2021
#PromiBB