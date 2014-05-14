import sqlite3 as sqlite

from libraries import imagesearch
from libraries import sift
from libraries import imtools
from libraries import vocabulary as voc

import math
import pickle
from numpy import *
from scipy.cluster.vq import *
from pylab import *

import sys

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

# connect with local database
con = sqlite.connect('vocab.db')

# get list of images
data = load('../tweets_instagram_final.pkl')
l = len(data)

for i in xrange(l):
	id_ = data[i]['id_str']
	image =  path + id_ + ext
	imlist.append(image)

nbr_images = len(imlist)
nr_div = 3
div = nbr_images/nr_div

matx = {}

print "Creating" + str(nr_div) + "matrix of zeros\n"

for w in xrange(nr_div):

	temp = "matx" + str(w)
	matx[temp] = [] #variables matx0 matx1 and matx3

	start_val = div * w
	end_val = div * (w+1)

	print "Matrix number ", w

	for k in xrange(div):
		arr = [0] * div
		matx[temp].append(arr)
		sys.stdout.write("\r" + str((k * (w+1)) + 1) + " of " + str(end_val))
		sys.stdout.flush()

	m = asarray(matx[temp])
	print "\nDone!\n"

	print "Start calculations and add values to matrix"
	r = 0 #row
	c = 0 #column
	for i in xrange(start_val, end_val):
		filename1 = imlist[i]
		imid1 = con.execute("select rowid from imlist where filename='%s'" % filename1 ).fetchone()
		cand_h1 = con.execute("select histogram from imhistograms where rowid='%d'" % imid1).fetchone()
		cand_h1 = pickle.loads(str(cand_h1[0]))
		for j in xrange(start_val, end_val):
			if i < j:
				filename2 = imlist[j]
				imid2 = con.execute("select rowid from imlist where filename='%s'" % filename2 ).fetchone()
				# get the histogram candidate
				cand_h2 = con.execute("select histogram from imhistograms where rowid='%d'" % imid2).fetchone()
				cand_h2 = pickle.loads(str(cand_h2[0]))
				cand_dist = math.sqrt( sum( (cand_h1 - cand_h2)**2 ) ) #use L2 distance
				m[r][c] = cand_dist
			c += 1
		r += 1
		c = 0 

		sys.stdout.write("\r" + str(i + 1) + " of " + str(end_val))
		sys.stdout.flush()

	print "\nEnd of calculations\n"

	print "Saving file..."
	# saving
	with open('./matrix_dist/matrix'+ str(w) +'_non_normalized.pkl', 'wb') as f:
	  pickle.dump(m,f)
	print "end!"


