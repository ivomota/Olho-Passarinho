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
# f = open('/Applications/MAMP/htdocs/Tese/Results/twitpic_urls_2.txt', 'w')
f = open('./resultados/twitpic_teste.json', 'w')

# data = []
id_tweet = '347038057221980162'

for data in collection.find({'id_str' : id_tweet}):
	f_data = json.dumps(data, default=json_util.default)
	f.write(f_data+'\n')

f.close()