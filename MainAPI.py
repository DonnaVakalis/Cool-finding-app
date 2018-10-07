# -*- coding: utf-8 -*-
"""

This finds the friends of a Twitter user, and stores them in a list; then, this list is passed back to find the friends-of-friends; 

The goal is to calculate overlaps and give an index of 'how much overlap' there is among your friends.
...Kind of like a quantification of how much your twitter feed is a 'bubble' 
 
Created on Fri Oct  5 14:53:20 2018

@author: Donna
"""

#%% Import useful files

import tweepy
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


import numpy 
import pandas  

import utils_do_not_post as ut  #This protects keys from viewing when sharing this code
# utils_do_not_post contains the following four variables:
# API key CONSUMER_KEY  
# API secret  CONSUMER_SECRET  
# Access token ACCESS_TOKEN  
# Access token secret  ACCESS_TOKEN_SECRET  

#%% Create Classes  

class TwitAuthenticator():
    """
    Authentication
    """
    def authenticate_twitter_app(self):
        #Connect on OAuth process, using the keys and tokens:
        auth = tweepy.OAuthHandler(ut.CONSUMER_KEY, ut.CONSUMER_SECRET) 
        auth.set_access_token(ut.ACCESS_TOKEN, ut.ACCESS_TOKEN_SECRET)
        return auth

class TwitClient():
    """
    Construct a client class...this is the one that gets the friends list :)
    """
    #Construct a Client 
    def __init__(self,twitter_user=None):
        self.auth = TwitAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user
        
    def get_twitter_client_api(self):
        return self.twitter_client
    
    def get_friend_list(self):
        friend_list=[]
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items():
            friend_list.append(friend)
        return friend_list
    
    def on_error(self, status):
        if status == 420:
            #Kill it if rate limit is exceeded
            return False
        print(status)

class FriendAnalyzer():
    """
    Listing and categorizing friends list
    """
    def friends_to_data_frame(self, friend_list):
        df = pandas.DataFrame(data=[friend.id for friend in friend_list], columns=['Friends ID'])

        df['Name'] = numpy.array([friend.name for friend in friend_list])
        #df['id'] = numpy.array([friend.id for friend in friend_list])
        df['Friends_count'] = numpy.array([friend.friends_count for friend in friend_list])

        return df
    
#%% Main part of the program

if __name__ == "__main__":
    
    twitter_client = TwitClient()
    friend_analyzer = FriendAnalyzer()

    api = twitter_client.get_twitter_client_api()
    friendList = twitter_client.get_friend_list()
    
    #print(dir(friendList[0]))    
    
    df = friend_analyzer.friends_to_data_frame(friendList)
    print(df.head(10))


     
    
       
   


#%%




