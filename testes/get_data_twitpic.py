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
#regx = re.compile("pic|twitpic|flic|instagram", re.IGNORECASE)
#regx = re.compile("^pic.twitter.com", re.IGNORECASE)
regx = re.compile("^twitpic.com", re.IGNORECASE)

# f = open('/Applications/MAMP/htdocs/Tese/Results/twitpic_urls_2.txt', 'w')
f = open('./resultados/twitpic_urls.sql', 'w')

data = []
vetor = []
twitpic = 0
# a = {}
count = 0
ret = 0
chave = False

# for each in collection.find( {'entities.urls.display_url' : { '$exists': True}}, { 'entities.urls.display_url' : 1} ):
# if each["entities"]["urls"][0]["display_url"].startswith('twitpic.com'):
# a[each['_id']] = each["entities"]["urls"][0]["display_url"]
    
for each in collection.find( {'entities.urls.display_url' : regx}):#, { 'entities.urls.display_url' : 1} ):
	# ID = each["_id"]
	ID = each["id_str"]
	
	URL = each["entities"]["urls"][0]["display_url"]
	try:
		RETWEET = each["retweeted_status"]
		ORIGINAL_TWEET = each['in_reply_to_status_id_str']
		ret = ret + 1
		chave = True
	except:
		chave = False

	m = re.search(r"^[^.]*", URL)
	site = m.group(0)
	n = re.search(r"com/(\w+)", URL)

	try:
		codigo = n.group(1)
		# print codigo
		if site == 'twitpic':
			try:
				if chave:
					if codigo in vetor:

						f.write("INSERT INTO imagens (id_objeto, servico, url, tipo, retweet) VALUES (""'"+str(ID)+"', '"+site+"', '"+URL+"', 'Retweet', 'NULO');\n")
					else:
						f.write("INSERT INTO imagens (id_objeto, servico, url, tipo, retweet) VALUES (""'"+str(ID)+"', '"+site+"', '"+URL+"', 'Retweet', 'Primeiro');\n")
						vetor.append(codigo)
				else:
					f.write("INSERT INTO imagens (id_objeto, servico, url, tipo, retweet) VALUES (""'"+str(ID)+ "', '"+site+"', '"+URL+"', 'Tweet', 'NULO');\n")
				twitpic = twitpic + 1 
			except:
				pass

	# f_data = json.dumps(f_data, default=json_util.default)
	# f.write(f_data+'\n')
		count = count + 1
		if count%1000 == 0:
			print count
	except:
		pass

print "Numero de urls twitpic --> " + str(twitpic)
print "Numero de retweets --> " + str(ret)
f.close()

