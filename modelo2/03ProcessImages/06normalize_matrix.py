from numpy import *
import pickle
import os

from rpy2.robjects import r
from rpy2.robjects.numpy2ri import numpy2ri


def getmax(myarray):
	return amax(myarray)

def getmean(myarray):
	return mean(myarray)

def getstd(myarray):
	return std(myarray)

def norm(myarray, value_mean, value_std):
	new_array = []
	row = []
	lenght = len(myarray[0])
	for x in range(lenght):
		for k in range(lenght):
			value = myarray[x][k]
			if x >= k:
				row.append(0)
			else:
				new_value = round((value - value_mean)/float(value_std), 3)
				row.append(new_value)

		new_array.append(row)
		row =[]
	new_array = asarray(new_array)

	return new_array

def getfiles(path):
    """    Returns a list of filenames for 
    all matrix non normalized in a directory. """
        
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('pkl')]

path = './matrix_im/'
files = getfiles(path)

for index, file in enumerate(files):
	# get matrix 
	matx = load(file)
	l = len(matx)

	# get the maximum value 
	# value_max = getmax(matx)
	value_mean = getmean(matx)
	value_std = getstd(matx)

	# print value_max
	# print value_mean
	# print value_std
	# print (value_max - value_mean)/ value_std

	mdist = norm(matx, value_mean, value_std)
	print mdist[0:9][0:9]


	transp = mdist.T
	print len(mdist)
	x1 = mdist.reshape((l,l))
	x2 = transp.reshape((l,l))
	mat = add(x1, x2)
	# print len(mat)
	

	mat = array(mat, dtype="float64") # <- convert to double precision numeric since R doesn't have unsigned ints
	ro = numpy2ri(mat)
	r.assign("bar", ro)
	r("saveRDS(bar, file='../matrix_dist_norm/sample"+ str(index) +"_im_dist_norm.rds')")


'''
extra code
'''
# mat = asmatrix(mat)
# print type(mat)

# f = open('R_Project_server/sample_ct_dist_norm0.rds', 'r+')
# f.write(str(mat))
# f.close()