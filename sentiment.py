import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import datetime
import matplotlib.pyplot as plt
from decimal import *

class SentimentAnalysis(object):
    p_tweets=0
    n_tweets=0
    neu_tweets=0
    total_tweets=0

    #initialize the object with user credentials
    def __init__(self):
        consumer_key = 'Ir9ESahvCSNaVWVdCrUCwmsf4'
        consumer_secret = 'bL7riSFQ1pXRAAqbHUgAyS4eI03Bg51xFnFUV19UJgLbjKCteS'
        access_key = '1169854323943038976-8xcs85UNeYyOK06stLNfyD5D8KjK0z'
        access_secret = '8P9yMTkrzgsbAUvn5YRMgfhybAut5Rl0nYhZp9VuidTur'
         
        try :
            self.auth = OAuthHandler(consumer_key,consumer_secret)
            self.auth.set_access_token(access_key,access_secret)
            self.api = tweepy.API(self.auth)
        except :
            print("Authentication failed\n")

    #clean the tweet by removing unwanted symbols
    def clean_tweet(self, tweet): 
            return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 


    #fetch the tweets and store them
    def fetch_tweets(self,query):
        startdate = datetime.date(2020,3,24)
        enddate   = datetime.date(2020,4,24)

        try:

          fetched_tweets = tweepy.Cursor(self.api.search,q=query + " -filter:retweets",lang="en",since=startdate,tweet_mode='extended',until=enddate).items()
          for tweet in fetched_tweets :
              self.total_tweets = self.total_tweets + 1
              self.AnalyseTweet(tweet.full_text)

        except tweepy.TweepError as e:
          print(str(e))

    def AnalyseTweet(self,tweet):
        res = TextBlob(self.clean_tweet(tweet))
        if res.sentiment.polarity > 0:
            self.p_tweets = self.p_tweets + 1
            
        if res.sentiment.polarity == 0:
            self.neu_tweets = self.neu_tweets + 1
            
        if res.sentiment.polarity < 0:
            self.n_tweets = self.n_tweets + 1
            

getcontext().prec=3
sa = SentimentAnalysis()

sa.fetch_tweets("#Google")

tweets_count = [ sa.p_tweets,
                 sa.n_tweets,
                 sa.neu_tweets ] 

labels = [ "Positive " + str(Decimal((sa.p_tweets / sa.total_tweets)) * 100) + " %",
           "Negative " + str(Decimal((sa.n_tweets / sa.total_tweets)) * 100) + " %" ,
           "Neutral " + str(Decimal((sa.neu_tweets / sa.total_tweets)) * 100) + " %" ]

plt.pie( tweets_count,
         labels=labels,
         colors=['g','r','y']
       )
plt.show()