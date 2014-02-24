# -*- encoding: utf-8 -*-

import cStringIO # *much* faster than StringIO 
from bson import json_util
import json
import re

import pymongo
from pymongo import MongoClient

print 'Starting Script...\n'

client = MongoClient('192.168.102.190')
print 'Connected to database...\n'
db = client.socialecho_br
collection = db.tweets

regx = re.compile("pic|twitpic|flic|instagram", re.IGNORECASE)

f = open('./resultados/data.json', 'w')
i = 0;

for d in collection.find({'entities.urls.display_url' : regx}):
	f_data = json.dumps(d, default=json_util.default)
	f.write(f_data+'\n')
	i = i + 1 
	if i % 100000 == 0:
		print i

print i

f.close()

