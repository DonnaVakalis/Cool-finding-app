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

#%%
import sys
sys.path.append('../')
for p in sys.path:
    print(p)


#%%
import time 
import numpy 
import pandas  
import utils_dnp


import importlib
importlib.reload(utils_dnp)
 
  
#This protects keys from viewing when sharing this code
# utils_do_not_post contains the following four variables:
# API key CONSUMER_KEY  
# API secret  CONSUMER_SECRET  
# Access token ACCESS_TOKEN  
# Access token secret  ACCESS_TOKEN_SECRET  


print(utils_dnp.CONSUMER_KEY) #Erase this line later: used for checking whether utils_dnp has been reloaded

#%% Create Classes  

class TwitAuthenticator(): 
    """
    Authentication, gets called inside TwitClient class
    """
    def authenticate_twitter_app(self):
        #Connect on OAuth process, using the keys and tokens:
        auth = tweepy.OAuthHandler(utils_dnp.CONSUMER_KEY, utils_dnp.CONSUMER_SECRET) 
        auth.set_access_token(utils_dnp.ACCESS_TOKEN, utils_dnp.ACCESS_TOKEN_SECRET)
        return auth

class TwitClient():
    """
    Construct a client. Get authorization from Twitter API. 
    And gets the friends list of the given twitter_user (not necessarily the same as the authorizing account!)
    """
    #Construct a Client 
    def __init__(self,twitter_user=None):
        self.auth = TwitAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user
        print(self.twitter_user) #for debugging purposes erase later
        
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
        df = pandas.DataFrame(data=[friend.id for friend in friend_list], columns=['Friend_ID'])

        df['Name'] = numpy.array([friend.name for friend in friend_list])
        df['User_name'] = numpy.array([friend.screen_name for friend in friend_list]) #broke after I added this line
        df['Friends_count'] = numpy.array([friend.friends_count for friend in friend_list])

        return df
    
    def count_ships(self):
        pass
    
#%% Main part of the program

if __name__ == "__main__":
    
    #Get List of 'Friends'    
    twitter_client = TwitClient()
    friend_analyzer = FriendAnalyzer()

    api = twitter_client.get_twitter_client_api()
    friendList = twitter_client.get_friend_list()
    
    #print(dir(friendList[0]))    #for finding attributes of object friendList (which is a list of built-in "friend" objects)
    
    MyFriends = friend_analyzer.friends_to_data_frame(friendList)
    print(MyFriends.head(12))
    #print(MyFriends.User_name[0])
    
    #%%
 
    #Get list of 'Friends' of 'Friends'  MyFriends.Name[0]
    #twitter_client = TwitClient(twitter_user=MyFriends.User_name[0]) #works with twitter_user="SportIsAllOver"
    vvv = "TheDickCavett"
    print(vvv)
    print(MyFriends.User_name[4])
    
    #%%
    twitter_client = TwitClient(twitter_user=MyFriends.User_name[4])
    #%%
    friend_analyzer = FriendAnalyzer()
    #%%
    friendList2 = twitter_client.get_friend_list()
    #%%
    TheirFriends = friend_analyzer.friends_to_data_frame(friendList2)
    print(TheirFriends.head(10))






