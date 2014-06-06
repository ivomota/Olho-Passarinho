import pickle
import math
from numpy import *
import sys

from rpy2.robjects import r
from rpy2.robjects.numpy2ri import numpy2ri

def load(filename, verbose=False):
    # Open file
    if verbose : print("Loading %s" % filename)
    pkl_file = open(filename, 'rb')
    # Load from Pickle file.
    data = pickle.load(pkl_file)
    pkl_file.close()
    return data

def hf(long1, lat1, long2, lat2):
	R = 6371 # Earth mean radius [km]
	delta_long = (long2 - long1)
	delta_lat = (lat2 - lat1)
  	a = sin(delta_lat/2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_long/2)**2
	c = 2 * arcsin(min(1,sqrt(a)))
	d = R * c
  	return d # Distance in km

def deg2rad(deg):
	return (deg*pi/180)


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
		long1 = deg2rad(data[i]['coordinates']['coordinates'][0])
		lat1 = deg2rad(data[i]['coordinates']['coordinates'][1])
		for j in xrange(start_val, end_val):
			if i < j:
				long2 = deg2rad(data[j]['coordinates']['coordinates'][0])
				lat2 = deg2rad(data[j]['coordinates']['coordinates'][1])
				dist = hf(long1, lat1, long2, lat2)
				m[r][c] = dist
			c += 1
		r += 1
		c = 0 

		sys.stdout.write("\r" + str(i + 1) + " of " + str(end_val))
		sys.stdout.flush()

	print "\nEnd of calculations\n"

	print "Saving file..."
	# saving
	with open('./matrix_spatial/matrix'+ str(w) +'_non_normalized.pkl', 'wb') as f:
	  pickle.dump(m,f)
	print "end!"







