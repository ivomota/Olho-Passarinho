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


f = open('./id_tweets.txt', 'read')
lst = f.read()
f.close()

print lst