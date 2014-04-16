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


lst = np.loadtxt('id_tweets.gz', delimiter=" ", dtype=(str))
# print lst


# for idt in lst:
# 	for each in collection.find( {'id_str': idt}, { 'geo' : {'$ne': None} } ):
# 		# print each['user']['id_str']
# 		print each['geo']
# 		i += 1
for x in xrange(20,25):
	i = 1
	vetor = []
	start = 1000 * x + 1
	end = start + 999 
	for j in xrange(start, end):
		for doc in collection.find({ '$and' :[ {'id_str': lst[j]}, { 'coordinates' : {'$ne': None} } ] }, {'coordinates.coordinates' : 1, 'created_at': 1, 'text': 1, 'user.id_str': 1, 'user.name': 1, 'entities.urls.display_url' : 1 }).limit(1):
			if doc:
				vetor.append(doc)
				i += 1
		# tpm = []
		# for elem in doc:
		# 	print j
		# 	i += 1
		# 	id_tweet = lst[j]
		# 	tpm.append(id_tweet)
		# 	lat = elem['coordinates']['coordinates'][0]
		# 	tpm.append(lat)
		# 	long = elem['coordinates']['coordinates'][1]
		# 	tpm.append(long)
		# 	time = elem['created_at']
		# 	tpm.append(time)
		# 	text = elem['text']
		# 	tpm.append(text)
		# 	user_id = elem['user']['id_str']
		# 	tpm.append(user_id)
		# 	user_name = elem['user']['name']
		# 	tpm.append(user_name)
		# 	url = elem['entities']['urls'][0]['display_url']
		# 	tpm.append(url)
		# if tpm:
		# 	vetor.append(tpm)
	print "file: data" + str(x) + "pkl"
	print "count: " + str(i)

	# saving
	with open('data'+ str(x) +'.pkl', 'wb') as f:
	  pickle.dump(vetor,f)


# vetor = np.array(vetor)
# np.savetxt('id_tweets.gz', vetor, delimiter=",", fmt="%s") 

# f = open('./exemplo2.json', 'w')
# f_data = json.dumps(doc[0], default=json_util.default)
# f.write(f_data+'\n')
# f.close()