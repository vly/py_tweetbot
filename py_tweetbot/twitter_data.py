import requests
from BeautifulSoup import BeautifulSoup
import json
from oauth_hook import OAuthHook
from urlparse import parse_qs
import sys
from time import sleep

from xml.dom.minidom import parseString

# constants
REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL  = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL        = 'https://api.twitter.com/oauth/authenticate'

class TwitterData:

    def __init__(self, settings):
        # variables
        self.consumer_key    = settings['consumer_key']
        self.consumer_secret = settings['consumer_secret']
        self.header_auth = True

    def load_user(self, user):
        self.oauth_token = user['oauth_token']
        self.oauth_token_secret = user['oauth_token_secret']
        self.access_token = user['access_token']
        self.access_token_secret = user['access_token_secret']
        self.oauth_pin = user['oauth_pin']

    def get_token(self):
        client = requests.session(hooks={'pre_request': OAuthHook(consumer_key=self.consumer_key, consumer_secret=self.consumer_secret)})
        response = client.get(REQUEST_TOKEN_URL)
        response = parse_qs(response.content)
        print "Token: %s Secret: %s" % (response['oauth_token'], response['oauth_token_secret'])
        self.oauth_token = response['oauth_token'].pop()
        self.oauth_token_secret = response['oauth_token_secret'].pop()

    def get_pin(self):
        print "Please go to: " + AUTHORIZATION_URL + "?oauth_token=" + self.oauth_token
        self.oauth_pin = raw_input("Enter pin: ")

    def get_access_token(self):
        print "Running access token retrieval"
        oauth_hook = OAuthHook(self.oauth_token, self.oauth_token_secret, self.oauth_pin, self.consumer_key, self.consumer_secret)
        client = requests.session(hooks={'pre_request': oauth_hook})
        response = client.get(ACCESS_TOKEN_URL)
        if response.status_code == 200:
            response = parse_qs(response.content)
            print response
            self.access_token = response['oauth_token'].pop()
            self.access_token_secret = response['oauth_token_secret'].pop()
        elif response.status_code == 401:
            error = parseString(response.content).getElementsByTagName("error")
            error = error[0].firstChild.data
            print "Error: ", error

    def test_get_access_token(self, block):
        print "Running access token retrieval"
        oauth_hook = OAuthHook(block['oauth_token'],block['oauth_token_secret'],block['oauth_pin'],self.consumer_key,self.consumer_secret)
        client = requests.session(hooks={'pre_request': oauth_hook})
        response = client.get(ACCESS_TOKEN_URL)
        if response.status_code == 200:
            response = parse_qs(response.content)
            print response
            self.access_token = response['oauth_token'].pop()
            self.access_token_secret = response['oauth_token_secret'].pop()
        elif response.status_code == 401:
            error = parseString(response.content).getElementsByTagName("error")
            error = error[0].firstChild.data
            print "Error: ", error

    def post_update(self, message):
        if len(message) > 140:
            print "The message is too long."
            sys.exit(1)
        oauth_hook = OAuthHook(self.access_token, self.access_token_secret, self.oauth_pin, self.consumer_key, self.consumer_secret)
        client = requests.session(hooks={'pre_request': oauth_hook})
        response = client.post('http://api.twitter.com/1/statuses/update.json', {'status': message, 'wrap_links': True})
        if response.status_code == 200:
            print "\"" + message + "\" " + "has been posted."
            return True
        else:
            print "Something went horribly wrong. ", response.content
            return False