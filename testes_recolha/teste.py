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

# f = open('./resultados/teste.txt', 'w')

data = []

count = 0
ret = 0

for each in collection.find( {'retweeted_status' : {'$exists': True}}): #, { 'entities.urls.display_url' : 1} ):
	# DATA = each

	try: 
		lang = each['retweeted_status']
		ret += 1 
	except:
		pass
	# try:
	# 	RETWEET = each["retweeted_status"]
	# 	ORIGINAL_TWEET = each['in_reply_to_status_id_str']
	# 	ret = ret + 1
	# 	chave = True
	# except:
	# 	chave = False

	# if chave:
	# 	f.write(ORIGINAL_TWEET +', Retweetado\n')
	# else:
	# 	f.write('NULL\n')
	count = count + 1 

	# f_data = json.dumps(each, default=json_util.default)
	# f.write(f_data+'\n')

print count
print ret
# f.close()
