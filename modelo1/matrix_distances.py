import sqlite3 as sqlite

import imagesearch
import sift
import imtools
import vocabulary as voc

import math
import pickle
from numpy import *
from scipy.cluster.vq import *
from pylab import *

from rpy2.robjects import r
from rpy2.robjects.numpy2ri import numpy2ri

def getmax(myarray):
	test = []
	lenght = len(myarray[0])
	for r in range(lenght):
		test.append(max(myarray[r]))

	return max(test)

def norm(myarray, value_max):
	new_array = []
	row = []
	lenght = len(myarray[0])
	for x in range(lenght):
		for k in range(lenght):
			value = myarray[x][k]
			if value == 0:
				row.append(0)
			else:
				row.append(value/value_max)
			
		new_array.append(row)
		row =[]
	new_array = asarray(new_array)

	return new_array



# get list of images
imlist = imtools.get_imlist('../img/img_test/') 
nbr_images = len(imlist)

con = sqlite.connect('test.db')

matchscores = []
row = []
a = 0

for i in range(nbr_images):
	filename1 = imlist[i]
	imid1 = con.execute("select rowid from imlist where filename='%s'" % filename1 ).fetchone()
	cand_h1 = con.execute("select histogram from imhistograms where rowid='%d'" % imid1).fetchone()
	cand_h1 = pickle.loads(str(cand_h1[0]))

	for j in range(nbr_images):
		if j>i:
			cand_dist = 0.0
			row.append(cand_dist)
		else:
			filename2 = imlist[j]
			imid2 = con.execute("select rowid from imlist where filename='%s'" % filename2 ).fetchone()
			# get the histogram candidate
			cand_h2 = con.execute("select histogram from imhistograms where rowid='%d'" % imid2).fetchone()
			cand_h2 = pickle.loads(str(cand_h2[0]))
			cand_dist = math.sqrt( sum( (cand_h1 - cand_h2)**2 ) ) #use L2 distance
			row.append(cand_dist)
	
	matchscores.append(row)
	row = []

myarray = asarray(matchscores)
# print myarray


value_max = getmax(myarray)
# print value_max

mdist = norm(myarray, value_max)

transp = mdist.T

# print len(mdist)
x1 = mdist.reshape((nbr_images,nbr_images))
x2 = transp.reshape((nbr_images,nbr_images))

mat = add(x1, x2)

mat = array(mat, dtype="float64") # <- convert to double precision numeric since R doesn't have unsigned ints
ro = numpy2ri(mat)
r.assign("bar", ro)
r("saveRDS(bar, file='R_Project_server/sample_ct_dist_norm.rds')")



# mat = asmatrix(mat)
# print type(mat)

# f = open('R_Project_server/sample_ct_dist_norm.rds', 'r+')
# f.write(str(mat))
# f.close()

