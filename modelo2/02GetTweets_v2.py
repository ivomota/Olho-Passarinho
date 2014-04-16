# -*- encoding: utf-8 -*-

import numpy as np
import cStringIO # *much* faster than StringIO 
from bson import json_util
import json
import re
import pickle

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


ids = np.loadtxt('id_tweets.gz', delimiter=" ", dtype=(str))
# print lst

ids = ids.tolist()

print type(ids)

i = 1
vetor = []


for doc in collection.find({ '$and' :[ {'id_str' :{'$in': ids}}, {'coordinates' : {'$ne': None} }] }, {'id_str': 1, 'coordinates.coordinates' : 1, 'created_at': 1, 'text': 1, 'user.id_str': 1, 'user.name': 1, 'entities.urls.display_url' : 1 }):
	if doc:
		vetor.append(doc)
		i += 1

print "count: " + str(i)

# saving
with open('tweets_instagram.pkl', 'wb') as f:
  pickle.dump(vetor,f)
