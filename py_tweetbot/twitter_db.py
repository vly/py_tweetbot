import sqlite3
import sys
import time

class TwitterDB:
    def __init__(self):
        self.open_db()

    def open_db(self):
        self.connection = sqlite3.connect("py_tweet.db")
        self.cursor = self.connection.cursor()

    def add_user(self, username):
        try:
            self.cursor.execute('INSERT INTO users VALUES(NULL, ?, NULL, NULL, NULL)', (username,))
            self.connection.commit()
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if self.cursor:
                self.cursor.close()

    def update_user(self, username, oauth_token=None, oauth_token_secret=None,
                    access_token=None, access_token_secret=None,
                    oauth_pin=None):
        try:
            self.cursor.open()
            self.cursor.execute('UPDATE users SET oauth_token=?, oauth_token_secret=?, access_token=?, access_token_secret=?, oauth_pin=? WHERE username=?', (oauth_token, oauth_token_secret, access_token, access_token_secret, oauth_pin, username))
            self.connection.commit()
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if self.cursor:
                self.cursor.close()

    def del_user(self, username):
        try:
            self.cursor.execute('DELETE FROM users WHERE username=?', (username,))
            connection.commit()
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if self.cursor:
                self.cursor.close()

    def get_user(self, username):
        """ Returns a dictionary of user settings (user_data). """
        try:
            self.open_db()
            self.cursor.execute('SELECT * FROM users WHERE username=?', (username,))
            user_data = self.cursor.fetchall()[0]
            user_data = {"uid" : user_data[0],
                         "username" : user_data[1],
                         "oauth_token" : user_data[2],
                         "oauth_token_secret" : user_data[3],
                         "access_token" : user_data[4],
                         "access_token_secret" : user_data[5],
                         "oauth_pin" : user_data[6]}
            return user_data
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if self.cursor:
                self.cursor.close()

    def get_all_users(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def get_settings(self):
        """ Returns a dictionary of all settings. """
        try:
            self.cursor.execute('SELECT * FROM settings')
            settings = self.cursor.fetchall()[0]
            settings = {"consumer_key" : settings[0],
                        "consumer_secret" : settings[1]
            }
            return settings
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if self.cursor:
                self.cursor.close()

    def add_settings(self, consumer_key, consumer_secret):
        self.cursor.execute('INSERT INTO settings VALUES(?,?)', (consumer_key, consumer_secret))
        self.connection.commit()

    def update_settings(self, consumer_key, consumer_secret):
        self.cursor.execute('UPDATE settings SET consumer_key=?, consumer_secret=?', (consumer_key, consumer_secret))
        self.connection.commit()

    def add_tweet(self, message):
        self.cursor.execute('INSERT INTO tweets VALUES(NULL,?)',(message,))
        self.connection.commit()

    def tweet_queue(self, limit=None):
        try:
            self.open_db()
            maximum = ""
            if limit is not None:
                maximum = "LIMIT " + str(limit)
            self.cursor.execute('SELECT * FROM tweets t WHERE t.tweetID NOT IN (SELECT tweetID FROM sent_tweets s)' + maximum)
            return self.cursor.fetchall()
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if self.cursor:
                self.cursor.close()

    def send_tweet(self, tweetID, uID):
        try:
            self.open_db()
            now = time.strftime('%X %x')
            self.cursor.execute('INSERT INTO sent_tweets VALUES(?,?,?)',(tweetID, uID, now))
            self.connection.commit()
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if self.cursor:
                self.cursor.close()

    def add_padding_tweet(self, message):
        self.cursor.execute('INSERT INTO padding_tweets VALUES(NULL,?)',(message,))
        self.connection.commit()

    def padding_tweet_queue(self, limit=None):
        try:
            self.open_db()
            maximum = ""
            if limit is not None:
                maximum = "LIMIT " + str(limit)
            self.cursor.execute('SELECT * FROM padding_tweets t WHERE t.pTweetID NOT IN (SELECT pTweetID FROM sent_padding_tweets s)' + maximum)
            return self.cursor.fetchall()
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if self.cursor:
                self.cursor.close()

    def send_padding_tweet(self, pTweetID, uID):
        try:
            self.open_db()
            now = time.strftime('%X %x')
            self.cursor.execute('INSERT INTO sent_padding_tweets VALUES(?,?,?)',(pTweetID, uID, now))
            self.connection.commit()
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if self.cursor:
                self.cursor.close()

    def close(self):
        self.cursor.close()