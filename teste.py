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
db = client.socialecho
collection = db.tweets

f = open('./resultados/teste.txt', 'w')

data = []

for each in collection.find( {'retweeted_status' : {'$exists': True}}, { 'entities.urls.display_url' : 1} ):
	# DATA = each
	f_data = json.dumps(each, default=json_util.default)
	f.write(f_data+'\n')

f.close()
