CREATE TABLE settings(
    consumer_key TEXT PRIMARY KEY,
    consumer_secret TEXT
    );

CREATE TABLE users(
    uID INTEGER PRIMARY KEY,
    username TEXT,
    oauth_token TEXT,
    oauth_token_secret TEXT,
    access_token TEXT,
    access_token_secret TEXT,
    oauth_pin TEXT
    );

CREATE TABLE tweets(
    tweetID INTEGER PRIMARY KEY,
    message TEXT
    );

CREATE TABLE sent_tweets(
    tweetID INTEGER,
    uID INTEGER,
    time DATE,
    FOREIGN KEY (tweetID) REFERENCES tweets(tweetID),
    FOREIGN KEY (uID) REFERENCES users(uID)
    );