#! /usr/bin/env python3

########################################################
#  Imports
########################################################

import twitter
import os
from datetime import datetime
import os
from urllib import parse as urlparse
import psycopg2

########################################################
#  Helper Functions
########################################################

def connect_to_twitter_api():
    # Get keys
    ck = os.environ.get('consumer_key')
    csec = os.environ.get('consumer_secret')
    ak = os.environ.get('access_token')
    asec = os.environ.get('access_token_secret')
    try:
        api = twitter.Api(consumer_key=ck,
                          consumer_secret=csec,
                          access_token_key=ak,
                          access_token_secret=asec)
        return(api)
    except:
        print("unable to connect to twitter api")


def connect_to_db():
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])

    # Determine if dev or production
    if (url.username):
        # Production
        try:
            conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
            return conn
        except:
            print("I am unable to connect to the database production")
    else:
        # Development
        try:
            conn = psycopg2.connect("dbname='michael' user='michael' host='localhost' password=''")
            return conn
        except:
            print("I am unable to connect to the database locally")

def get_linenum_from_db(db):
    cur = db.cursor()
    try:
        cur.execute("""SELECT * from lines""")
        rows = cur.fetchall()
        line = rows[0][1]
        cur.close()
        return line
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def update_db(db, prevlinenum):

    line_number = prevlinenum + 1

    try:
        sql = "UPDATE lines SET line_number = " + str(line_number) +  " WHERE id = 1"
        cur = db.cursor()
            # execute the UPDATE  statement
        cur.execute(sql)
        db.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def open_walden_file():
    f = open('walden.txt', 'r')
    data = f.readlines()
    f.close()
    return data

def split_tweet(s, n):
    for start in range(0, len(s), n):
        yield s[start:start+n]

def post_tweet(tweet, api):
    if (len(tweet) > 139):
        for chunk in split_tweet(tweet, 139):
            status = api.PostUpdate(chunk)
            print(status.text)
    else:
        status = api.PostUpdate(tweet)
        print(status.text)

########################################################
#  Script
########################################################

def main():
    try:
        # Connect
        db = connect_to_db()

        # Get current line number, then increment
        linenum = get_linenum_from_db(db)
        update_db(db, linenum)

        # Open waldex.txt
        data = open_walden_file()
        tweet = data[linenum]
        api = connect_to_twitter_api()
        post_tweet(tweet, api)
    except:
        print("Failed to post tweet")

main()
