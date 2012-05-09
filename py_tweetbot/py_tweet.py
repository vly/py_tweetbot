import socks
import socket

# init socks proxy
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 443)
socket.socket = socks.socksocket

# !important requests is called after socks init, as it replaces the default
import twitter_data
import twitter_db
import sys
from time import sleep

# some constants
PADDING_RATIO = 3 # 1:3 ratio of @ and padding tweets
BASE_DELAY = 3 # 3 seconds delay between tweets
RANDOMISE_DELAY = True # randomise the time delay between tweets
MULTI_USERS = False # use multiple accounts for tweeting
HOURLY_RATE = 100 # max number of tweets for each account per hour
APPLICATION_ID = "Tweet-o-matic v0.1" # app name identifier in API calls 


class TweetBot:
    def __init__(self):
        print "[Starting TwitterBot]"
        self.db = twitter_db.TwitterDB()
        self.load_settings()
        self.tdata = twitter_data.TwitterData(settings)

    def load_settings(self):
        """ Load Twitter API consumer key/secret pair. """
        self.settings = db.get_settings()
        if len(self.settings) < 2:
            while(True):
                consumer_key = raw_input("Enter your consumer key")
                consumer_secret = raw_input("Enter your consumer_secret")
                if len(consumer_key) > 5 and len(consumer_secret) > 5:
                    db.add_settings(consumer_key, consumer_secret)
                    break

    def get_user_list(self):
        """ Displays list of users in the DB and force selection. """
        self.user_list = db.get_user_list()
        for each in self.user_list:
            print each[1] # username
        while(True):
            selection = raw_input("Enter username to use")
            if selection in self.user_list:
                return selection


    def load_user_data(self, user=None):
        """ Pulls user data store in DB, gen new tokens/pin if none set."""
        if user is None:
            user = self.get_user_list()
        user_data = self.db.get_user(user)
        self.tdata.load_user(user_data)
        if user_data["oauth_token"] is None and user_data["oauth_token_secret"] is None:
            self.tdata.get_token()
        if user_data["oauth_pin"] is None:
            self.tdata.get_pin()
        if user_data["access_token"] is None and user_data["access_token_secret"] is None:
            self.tdata.get_access_token()
        self.user_data = user_data

    def generate_tweets_queue(self, limit=HOURLY_RATE):
        """ Generate list of tweets to run through."""
        tweet_list = self.db.tweet_queue(limit)
        padding_list = self.db.padding_tweet_queue(limit * PADDING_RATIO)
        if len(padding_list) < len(tweet_list) * PADDING_RATIO:
            print "Not enough padding tweets to maintain tweeting ratio."
        else:
            return {"tweets" : tweet_list, "padding" : padding_list}

    def start_queue(self):
        """ Init lists and update sequentially. """
        working_list = self.generate_tweets_queue()
        tweet_list = working_list["tweets"]
        padding_list = working_list["padding"]

        for tweet in tweet_list:
            counter = PADDING_RATIO
            # main tweet
            post = self.tdata.post_update(tweet[1])
            if post:
                print "\"" + tweet[1] + "\" tweet updated successfully."
                self.tdata.send_tweet(tweet[0], self.user_data["uid"])
            else:
                print "Failed to send... exiting."
                sys.exit(1)
                # padding updates
            while(counter > 0):
                sleep(BASE_DELAY)
                pad_tweet = padding_list.pop()
                post = self.tdata.post_update(pad_tweet[1])
                if post:
                    print "\"" + pad_tweet[1] + "\" padding tweet updated successfully."
                    self.tdata.send_padding_tweet(pad_tweet[0], self.user_data["uid"])
                    counter -= 1
                else:
                    print "Failed to update padding tweet... exiting."
                    sys.exit(1)
