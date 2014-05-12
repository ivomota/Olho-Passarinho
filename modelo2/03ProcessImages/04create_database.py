import pickle 
from libraries import sift
from libraries import imagesearch
from libraries import imtools
import sys
from numpy import *


# get list of images
imlist = imtools.get_imlist('./img/') 
nbr_images = len(imlist)
featlist = [ imlist[i][:-4]+'sift' for i in range(nbr_images) ]

# load vocabulary
with open('vocabulary.pkl', 'rb') as f:
  voc = pickle.load(f)

# create indexer
indx = imagesearch.Indexer('vocab.db',voc)
indx.create_tables()

error = []
print "First round"
end_val = nbr_images
# go through all images, project features on vocabulary and insert
for i in xrange(nbr_images):
	locs,descr = sift.read_features_from_file(featlist[i])
	if isinstance(descr, ndarray): 
		indx.add_to_index(imlist[i],descr)
	else:
		error.append(imlist[i])

	percent = float(i) / end_val
	bar_length = 20
	hashes = '=' * int(round(percent * bar_length))
	spaces = ' ' * (bar_length - len(hashes))
	sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
	sys.stdout.flush()

w = open('im_to_rm.txt', 'w')
w.write(str(error))
w.close()

# print "Last i: ", i

# print "Secound commit"
# end_val = nbr_images
# # go through all images, project features on vocabulary and insert
# for i in xrange(nbr_images/2, nbr_images):
# 	locs,descr = sift.read_features_from_file(featlist[i]) 
# 	indx.add_to_index(imlist[i],descr)

# 	percent = float(i) / end_val
# 	bar_length = 20
# 	hashes = '=' * int(round(percent * bar_length))
# 	spaces = ' ' * (bar_length - len(hashes))
# 	sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
# 	sys.stdout.flush()


# commit to database
indx.db_commit()


