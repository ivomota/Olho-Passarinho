import pickle
import os

def load(filename, verbose=False):
    # Open file
    if verbose : print("Loading %s" % filename)
    pkl_file = open(filename, 'rb')
    # Load from Pickle file.
    data = pickle.load(pkl_file)
    pkl_file.close()
    return data

data = load('../tweets_instagram_final.pkl')
length = len(data)
print "Total Tweets: ",  length

w = open('im_to_rm.txt', 'r')
file = w.read()
w.close()

file = eval(file)
nr_elem = len(file)
print "Number of files to remove: ", nr_elem
elem_to_remove = []

for elem in file:
	#Remove sift file
	try:
		os.remove(elem)	
	except:
		print "Nao existe ficheiro"
	#Remove jpeg file
	image = elem[:-4] + 'jpeg'
	try:
		os.remove(image)
	except:
		print "Nao existe ficheiro"
	#Remove tweet in data
	print "yooo"
	to_remove = elem.split('/')[-1]
	to_remove = to_remove.split('.')[0]
	for i in xrange(length):
		this = data[i]['id_str']
		if this == to_remove:
			elem_to_remove.append(file.index(elem))
			del data[i]
			break
	length = len(data)

print "New Total Tweets: ", length

# saving
with open('../tweets_instagram_final.pkl', 'wb') as f:
  pickle.dump(data,f)

offset = 0
for k in elem_to_remove:
	del file[k-offset]
	offset += 1 

print file

w = open('im_to_rm.txt', 'w')
w.write(str(file))
w.close()



