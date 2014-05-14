import pickle
import math
from numpy import *
import sys

from rpy2.robjects import r
from rpy2.robjects.numpy2ri import numpy2ri

from datetime import datetime
from dateutil import parser


def load(filename, verbose=False):
    # Open file
    if verbose : print("Loading %s" % filename)
    pkl_file = open(filename, 'rb')
    # Load from Pickle file.
    data = pickle.load(pkl_file)
    pkl_file.close()
    return data

data = load('../tweets_instagram_final.pkl')
leng = len(data)

nr_div = 3
div = leng/nr_div
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
		t1 = str(data[i]['created_at'])
		d1 = parser.parse(t1)
		for j in xrange(start_val, end_val):
			if i < j:
				t2 = str(data[j]['created_at'])
				d2 = parser.parse(t2)
				dist = abs((d2 - d1).total_seconds())
				m[r][c] = dist
			c += 1
		r += 1
		c = 0 

		sys.stdout.write("\r" + str(i + 1) + " of " + str(end_val))
		sys.stdout.flush()

	print "\nEnd of calculations\n"

	print "Saving file..."
	# saving
	with open('./matrix_temporal/matrix'+ str(w) +'_non_normalized.pkl', 'wb') as f:
	  pickle.dump(m,f)
	print "end!"







