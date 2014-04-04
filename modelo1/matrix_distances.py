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
imlist = imtools.get_imlist('../img/sunsets/treino/') 
nbr_images = len(imlist)

con = sqlite.connect('test.db')

matchscores = []
row = []
a = 0

for i in range(0, 5):
	filename1 = imlist[i]
	imid1 = con.execute("select rowid from imlist where filename='%s'" % filename1 ).fetchone()
	cand_h1 = con.execute("select histogram from imhistograms where rowid='%d'" % imid1).fetchone()
	cand_h1 = pickle.loads(str(cand_h1[0]))

	for j in range(0, 5):
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
x1 = mdist.reshape((5,5))
x2 = transp.reshape((5,5))

print add(x1, x2)
