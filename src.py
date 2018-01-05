#! /usr/bin/env python3

import twitter
#import random
import os
from datetime import datetime
#random.seed(datetime.now())

# Get env
ck = os.environ.get('consumer_key')
csec = os.environ.get('consumer_secret')
ak = os.environ.get('access_token')
asec = os.environ.get('access_token_secret')

api = twitter.Api(consumer_key=ck,
                      consumer_secret=csec,
                      access_token_key=ak,
                      access_token_secret=asec)


f = open('./walden.txt', 'r')
data = f.readlines()
f.close()

linenum = int(os.environ.get('line_number'))

if(linenum > len(data)):
    os.environ['line_number'] = str(0)
else:
    os.environ['line_number'] = str(int(linenum) + 1)

# parse data
tweet = data[linenum]

def chunks(s, n):
    for start in range(0, len(s), n):
        yield s[start:start+n]


if (len(tweet) > 139):
    for chunk in chunks(tweet, 139):
        status = api.PostUpdate(line)
        print(status.text)
else:
    status = api.PostUpdate(line)
    print(status.text)
