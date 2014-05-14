import pickle 
import sys
import os

from libraries import imtools

def load(filename, verbose=False):
    # Open file
    if verbose : print("Loading %s" % filename)
    pkl_file = open(filename, 'rb')
    # Load from Pickle file.
    data = pickle.load(pkl_file)
    pkl_file.close()
    return data

path = './img/'
ext = '.jpeg'
imlist = []
matx = {}

# get list of images
data = load('../tweets_instagram_final.pkl')
l = len(data)


# for i in xrange(l):
# 	id_ = data[i]['id_str']
# 	image =  path + id_ + ext
# 	imlist.append(image)

# nbr_images = len(imlist)
# div = (nbr_images/3)
## print len(imlist[0:div])
## print len(imlist[div:div*2])
## print len(imlist[div*2:div*3])

# for j in range(3):
# 	temp = "matx" + str(j)
# 	matx[temp] = []
# 	start_val = div * j
# 	end_val = div * (j+1)
# 	print start_val
# 	print end_val


