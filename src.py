#! /usr/bin/env python3

import twitter
import random
import os
from datetime import datetime
random.seed(datetime.now())

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

val = random.randint(0, len(data)-1)
line = (data[val])

status = api.PostUpdate(line)
print(status.text)
