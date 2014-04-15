# -*- encoding: utf-8 -*-

import numpy as np
import cStringIO # *much* faster than StringIO 
from bson import json_util
import json
import re

import pymongo
from pymongo import MongoClient

print 'Starting Script...\n'
try:
	client = MongoClient('192.168.102.190')
	print 'Connected to database...\n'
	db = client.socialecho_br
	collection = db.tweets
except Exception, e:
	print "An error occurred:", e.args[0]


lst = np.loadtxt('id_tweets.gz', delimiter=" ", dtype=(str))
# print lst


# for idt in lst:
# 	for each in collection.find( {'id_str': idt}, { 'geo' : {'$ne': None} } ):
# 		# print each['user']['id_str']
# 		print each['geo']
# 		i += 1
i = 1

for j in range(len(lst)):
	doc = collection.find({ '$and' :[ {'id_str': lst[j]}, { 'coordinates' : {'$ne': None} } ] }, {'coordinates' : 1, 'created_at': 1, 'text': 1, 'user': 1 }).limit(1)
	for elem in doc:
		print j
		print i
		i += 1
		# print elem['coordinates']['coordinates']
		# print elem['created_at']
		# print elem['text']
		# print elem['user']['id']
		# print elem['user']['name']

print "final: " + i

		# print j

# f = open('./exemplo2.json', 'w')
# f_data = json.dumps(doc[0], default=json_util.default)
# f.write(f_data+'\n')
# f.close()