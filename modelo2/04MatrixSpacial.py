import pickle
import math


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

# Convert degrees to radians
deg2rad <- function(deg) return(deg*pi/180) ##r script

data = load('tweets_instagram.pkl')
leng = len(data)

for i in xrange(leng):
	long1 = data[i]['coordinates']['coordinates'][0]
	lat1 = item[i]['coordinates']['coordinates'][1]
	for j in xrange(leng):
		long2 = data[j]['coordinates']['coordinates'][0]
		long2 = data[j]['coordinates']['coordinates'][0]






