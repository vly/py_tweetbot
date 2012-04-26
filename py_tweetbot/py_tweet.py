import socks
import socket

# init socks proxy
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 443)
socket.socket = socks.socksocket

# !important requests is called after socks init, as it replaces the default
import twitter_data
import twitter_db
from time import sleep

# config block
api_settings = {
        "consumer_key": "JQgjpOiIgwX7JIXK0hviQ",
        "consumer_secret":"0pHDdnDMaQzOh7lLFeZOEHeJzXRX9DNPuTKuSNEko",
        }

print "Starting twitter spammer:"

# db.update_user("val_lyashov",
#     api_settings['access_token'],
#     api_settings['access_token_secret'],
#     api_settings['oauth_pin'])
""" Initial settings config - assuming they don't change per app."""
# db.add_settings(api_settings['consumer_key'], api_settings['consumer_secret'],
#                 api_settings['oauth_token'], api_settings['oauth_token_secret'])
# """ Various 3 legged calls."""
# control.get_token()
# control.get_pin()
# control.get_access_token()

user_data = {"oauth_pin" : "3859659",
    "oauth_token" : "hx9qxj7RsvnQOnmAqEZjXoFUrqAj436wqwKHyDUdzdk",
    "oauth_token_secret" : "4NdzqIeZeJZYpVUqKKZ42KpHTsp4QLsKIZcHhykhXQ",
    "access_token" : "554877503-hmzCkaOdP9veohFL8BCprRftX7vE4S6eQgiGxJwg",
    "access_token_secret" : "PP3Pdyyq4WZ4cvJG8dK5aec8INKE6IZ4lus5gBMbX4",
    "uid" : "GiantLeap125"
    }

""" DB data retrieval. """
db = twitter_db.TwitterDB()
settings = db.get_settings()
user_data =  db.get_user("EXAMPLE")
db.close()


""" Twitter updates. """
control = twitter_data.TwitterData(settings)
# control.get_token()
# control.get_pin()
# control.get_access_token()
# control.test_get_access_token(user_block)

control.load_user(user_data)

""" Start tweeting."""
go = True
while go:
     max_tweets = 100
     temp_list =  db.tweet_queue(max_tweets)
     if len(temp_list) < 100:
         go = False
     for message in temp_list:
        res = control.post_update(message[1])
        print message
        if res:
             db.send_tweet(message[0], user_data['uid'])
        sleep(3) # 3 second delay between tweets
     sleep(3600) # sleep for an hour
