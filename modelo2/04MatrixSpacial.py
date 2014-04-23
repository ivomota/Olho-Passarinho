import pickle
import math
from numpy import *

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
	delta_lat <- (lat2 - lat1)
  	a = sin(delta_lat/2)^2 + cos(lat1) * cos(lat2) * sin(delta_long/2)^2
	c <- 2 * asin(min(1,sqrt(a)))
	d = R * c
  	return d # Distance in k

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
	# new_array = asarray(new_array)

	return new_array

# Convert degrees to radians
deg2rad <- function(deg) return(deg*pi/180) ##r script

data = load('tweets_instagram_final.pkl')
leng = len(data)

myarray = []

for i in xrange(leng):
	row = []
	long1 = data[i]['coordinates']['coordinates'][0]
	lat1 = item[i]['coordinates']['coordinates'][1]
	for j in xrange(leng):
		long2 = data[j]['coordinates']['coordinates'][0]
		long2 = data[j]['coordinates']['coordinates'][0]
		dist = hf(long1, lat1, long2, lat2)
		row.append(dist)
	myarray.append(row)

value_max = getmax(myarray)
mdist = norm(myarray, value_max) 

transp = mdist.T

# print len(mdist)
x1 = mdist.reshape((nbr_images,nbr_images))
x2 = transp.reshape((nbr_images,nbr_images))

matx = add(x1, x2)

mat = array(mat, dtype="float64") # <- convert to double precision numeric since R doesn't have unsigned ints
ro = numpy2ri(mat)
r.assign("bar", ro)
r("saveRDS(bar, file='R_Project_server/sample_sp_dist.rds')")







