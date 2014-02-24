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
regx = re.compile("^twitpic|^pic|^instagram", re.IGNORECASE)

# f = open('/Applications/MAMP/htdocs/Tese/Results/twitpic_urls_2.txt', 'w')
f = open('./resultados/insert_data.sql', 'w')

data = []
vetor = []

#Iniciação das variaveis da contagem das imagens de cada servico
twitpic = 0
pic = 0
insta = 0

count = 0
ret = 0
chave = False
insert = False

# for each in collection.find( {'entities.urls.display_url' : { '$exists': True}}, { 'entities.urls.display_url' : 1} ):
# if each["entities"]["urls"][0]["display_url"].startswith('twitpic.com'):
# a[each['_id']] = each["entities"]["urls"][0]["display_url"]
    
for each in collection.find( {'entities.urls.display_url' : regx}).limit(10000):
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

	if site == "pic":
		try:
			codigo = n.group(1)
			pic+=1
			insert = True
		except:
			insert = False
	elif site == "twitpic":
		try:
			codigo = n.group(1)
			twitpic+=1
			insert = True
		except:
			insert = False
	elif site == "instagram":
		try:
			codigo = n.group(1)
			insta+=1
			insert = True
		except:
			insert = False
	else:
		insert = False
	
	if insert:
		try:
			if chave:
				if codigo in vetor:
					f.write("INSERT INTO IMAGENS (id_tweet, servico, url, tipo, retweet) VALUES (""'"+str(ID)+"', '"+site+"', '"+URL+"', 'retweet', 'NULO');\n")
				else:
					f.write("INSERT INTO IMAGENS (id_tweet, servico, url, tipo, retweet) VALUES (""'"+str(ID)+"', '"+site+"', '"+URL+"', 'retweet', 'primeiro');\n")
					vetor.append(codigo)
			else:
				f.write("INSERT INTO IMAGENS (id_tweet, servico, url, tipo, retweet) VALUES (""'"+str(ID)+ "', '"+site+"', '"+URL+"', 'tweet', 'NULO');\n")
		except:
			pass

	count = count + 1
	if count%1000 == 0:
		print count

print "_________________________________________________"
print "Serviço: Twitpic\n"
print "Numero de urls --> " + str(twitpic)
print "\n"
print "_________________________________________________"
print "Serviço: Pic\n"
print "Numero de urls --> " + str(pic)
print "\n"
print "_________________________________________________"
print "Serviço: Instagram\n"
print "Numero de urls --> " + str(insta)
print "\n"


f.close()

