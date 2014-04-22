import pickle
import numpy as np
from bson import json_util
import json

# import itertools


'''
Load data
Remove duplicates
Save to json file

'''

def load(filename, verbose=False):
    # Open file
    if verbose : print("Loading %s" % filename)
    pkl_file = open(filename, 'rb')
    # Load from Pickle file.
    data = pickle.load(pkl_file)
    pkl_file.close()

    return data

# file = load('data_teste.pkl')
file = load('tweets_instagram.pkl')
print len(file)

# Remove duplicates without itertools
seen_values = set()
new_file = []
other = []
for d in file:
    value = d["id_str"]
    if value not in seen_values:
		new_file.append(d)
		seen_values.add(value)
    else:
    	other.append(value) #para debug
    
# print other
# print len(other)


# Remove duplicates with itertools (nao apaga 2 duplicados)
# new_file = [g.next() for k,g in itertools.groupby(file, lambda x: x['id_str'])]

#debug
# seen_values = set()
# other = []
# for d in new_file:
#     value = d["id_str"]
#     if value not in seen_values:
# 		seen_values.add(value)
#     else:
#     	other.append(value)
# print other

print len(new_file)

# saving
with open('tweets_instagram_clear.pkl', 'wb') as f:
  pickle.dump(new_file,f)

# f = open('tweets_instagram_exemple.json', 'w')
# f_data = json.dumps(new_file[0], default=json_util.default)
# f.write(f_data)
# f.close()
