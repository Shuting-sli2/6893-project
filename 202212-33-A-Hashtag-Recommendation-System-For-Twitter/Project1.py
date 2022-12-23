#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import json
import tweepy
import configparser
from datetime import datetime
import math
import requests


# In[3]:


def Twitter_tweets(userid, Token):
    global ss
    ss = 0
    global months
    global monthsrun
    months = [31,59,90,120,151,181,212,243,273,304,334,365]
    monthsrun = [31,60,91,121,152,182,213,244,274,305,335,366]
    global max_result
    max_result = 100
    # To set your environment variables in your terminal run the following line:
    # export 'BEARER_TOKEN'='<your_bearer_token>'
    global bearer_token
    bearer_token = Token
    global s_url
    s_url = "https://api.twitter.com/2/tweets/counts/recent"
    global s_query_params
    s_query_params = {'query': '#NFL','granularity': 'day'}
    
    hashtag = []
    index = 0
    tina = 0
    if True:
        while(True):
            tina = main(index,userid)
            a = tina.split('\n')
            info = []
            time = []
            getnum = int(a[-3].split(":")[1])
            for i in range(getnum):
                info.append(a[8*(i+1)])
                time.append(a[8*(i+1)-5])
            for i in range(len(info)):
                temp = info[i].split()
                for m in range(len(temp)):
                    if temp[m][0] == "#":
                        aka = temp[m].split("\\n")
                        hashtag.append([aka[0], 1, time[i]])
            if a[-4].split(":")[0].split('"')[1] == "oldest_id" and a[-5].split(":")[0].split('"')[1] != "newest_id":
                index = a[-5].split(":")[1].split('"')[1]
            elif a[-6].split(":")[0].split('"')[1] == "next_token":
                index = a[-6].split(":")[1].split('"')[1]
            else:
                break
            if ss == 3:
                break
            else:
                ss += 1

        hashtag = modify_hashtag(hashtag)
        hashtag_dict = sort_hashtag(hashtag)
        hashtag_dict = hastag_importance(hashtag_dict)
        hashtag_imp_sorted = dict(sorted(hashtag_dict.items(), reverse=True, key=lambda item: item[1]))
        jsonf = []
        for i in hashtag_imp_sorted:
            s_query_params['query'] = i
            try:
                search = json.dumps(s_connect_to_endpoint(s_url, s_query_params), indent=4, sort_keys=True)
                search_count = int(search.split("\n")[-7].split(":")[1])
                print("search_count", search_count)
                jsonf.append({"name": i, "tweet_volume": search_count, "weight": hashtag_imp_sorted[i]})
            except:
                pass
        #print(jsonf)
        with open("Twitter_Tweets.json", "w") as f:
            json.dump(jsonf, f, indent = 3)

def create_url(userid):
    # Replace with user ID below
    user_id = userid
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at", "max_results": 100}

def get_paramsnxt(key):
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at", "max_results": max_result, "pagination_token": key}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r

def s_bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentTweetCountsPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def s_connect_to_endpoint(url, params):
    response = requests.request("GET", s_url, auth=s_bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def modify_hashtag(hashtag):
    now = datetime.now()
    date = str(now).split(" ")[0].split("-")
    year = int(date[0])
    if int(date[0])%4 == 0:
        date = monthsrun[int(date[1])-1] + int(date[2])-31
        date = date*24*60
    else:
        date = months[int(date[1])-1] + int(date[2])-31
        date = date*24*60
    time = str(now).split(" ")[1].split(":")
    time = int(time[0])*60+int(time[1])
    mins = date + time
    for i in range(len(hashtag)):
        temp_date = hashtag[i][2].split('"')[3].split("T")[0].split("-")
        temp_year = int(temp_date[0])
        if int(temp_date[0])%4 == 0:
            temp_date = monthsrun[int(temp_date[1])-1] + int(temp_date[2])-31
            temp_date = temp_date*24*60
        else:
            temp_date = months[int(temp_date[1])-1] + int(temp_date[2])-31
            temp_date = temp_date*24*60
        temp_time = hashtag[i][2].split('"')[3].split("T")[1].split(":")
        temp_time = int(temp_time[0])*60+int(temp_time[1])
        temp_mins = temp_date + temp_time

        diff_year = 0
        for m in range(year-temp_year):
            if (temp_year+m)%4 == 0:
                diff_year += 366*24*60
            else:
                diff_year += 365*24*60

        total_diff = diff_year + mins - temp_mins + 300
        hashtag[i][2] = total_diff
    return hashtag

def sort_hashtag(hashtag):
    hashtag_dict = {}
    for i in range(len(hashtag)):
        if hashtag[i][0] in hashtag_dict:
            hashtag_dict[hashtag[i][0]][0] += 1
            hashtag_dict[hashtag[i][0]][1].append(hashtag[i][2])
        else:
            hashtag_dict[hashtag[i][0]] = [1, [hashtag[i][2]]]
    return hashtag_dict


def hashtag_decade(l):
    importance = 0
    for i in range(len(l)):
        #importance += math.exp(-0.5*l[i]/60/24)
        importance += (l[i]/60/24)**(-1.7)
    return math.log(importance)


def hastag_importance(hashtag_dict):
    for i in hashtag_dict:
        importance = hashtag_decade(hashtag_dict[i][1])
        hashtag_dict[i] = importance
    return hashtag_dict

def dict2list(dict):
    l = []
    for i in dict:
        l.append([i,dict[i]])
    return l

def main(index, userid):
    url = create_url(userid)
    if index == 0:
        params = get_params()
    else:
        params = get_paramsnxt(index)
    json_response = connect_to_endpoint(url, params)
    #print(json.dumps(json_response, indent=4, sort_keys=True))
    return json.dumps(json_response, indent=4, sort_keys=True)


# In[ ]:




