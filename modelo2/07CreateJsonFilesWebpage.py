import pickle 
import sys
import os
import json
from bson import json_util

def load(filename, verbose=False):
    # Open file
    if verbose : print("Loading %s" % filename)
    pkl_file = open(filename, 'rb')
    # Load from Pickle file.
    data = pickle.load(pkl_file)
    pkl_file.close()
    return data

path_dst = './Webpage/static/data'

# get list of images
data = load('./tweets_instagram_final.pkl')
lg = len(data)
print "Numero de tweets: ", lg

nr_div = 3
div = lg/nr_div

start = 0
end = div
# print start
# print end
s0 = data[start:end]
start = end
end = end + div
# print start
# print end
s1 = data[start:end]
start = end
end = end + div
# print start
# print end
s2 = data[start:end]

print "Subset0 tem: ", len(s0)
print "Subset1 tem: ", len(s1)
print "Subset2 tem: ", len(s2)

s0 = json_util.dumps(s0, default=json_util.default)
f0 = open('./Webpage/static/data/s0.json', 'w')
f0.write(str(s0))
f0.close()

s1 = json_util.dumps(s1, default=json_util.default)
f1 = open('./Webpage/static/data/s1.json', 'w')
f1.write(str(s1))
f1.close()

s2 = json_util.dumps(s2, default=json_util.default)
f2 = open('./Webpage/static/data/s2.json', 'w')
f2.write(str(s2))
f2.close()
