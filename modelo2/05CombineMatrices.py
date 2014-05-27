import os
from numpy import *
from rpy2.robjects import r
import rpy2.robjects.numpy2ri as rpyn


def getfiles(path):
    """    Returns a list of filenames for 
    all matrix non normalized in a directory. """
        
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.rds')]

def calculate(subset, w0, w1, w2, sub):
	mat_im = subset[0]
	mat_spat = subset[1]
	mat_temp = subset[2]
	# print subset0[:3][:3]
	# print subset1[:3][:3]
	# print subset2[:3][:3]

	l = len(w1)
	dim = len(subset[0])
	new_mat = zeros((dim, dim))
	# print new_mat[:3][:3]
	for i in range(l):
		for y in xrange(dim):
			for x in xrange(dim):
				new_mat[y][x] = w0[i] * mat_im[y][x] + w1[i] * mat_spat[y][x] + w2[i] * mat_temp[y][x]

		mat = array(new_mat, dtype="float64") # <- convert to double precision numeric since R doesn't have unsigned ints
		ro = rpyn.numpy2ri(mat)
		r.assign("bar", ro)
		r("saveRDS(bar, file='./matrix_combined/S"+ str(sub) +"/combined_matrix_"+ str(w0[i]) +"_"+ str(w1[i]) +"_"+ str(w2[i]) +".rds')")


w0 = [1, 0.75, 0.75, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0, 0, 0, 0, 0]
w1 = [0, 0.25, 0, 0.5, 0.25, 0, 0.75, 0.5, 0.25, 0, 1, 0.75, 0.5, 0.25, 0]
w2 = [0, 0, 0.25, 0, 0.25, 0.5, 0, 0.25, 0.5, 0.75, 0, 0.25, 0.5, 0.75, 1]
path = './matrix_dist_norm/'
files = getfiles(path)

subset0 = []
subset1 = []
subset2 = []

print "Subset 0"
for index, file in enumerate(files[:3]):
	sub = 0
	m = r("readRDS('"+ str(file)+"')")
	mat = rpyn.ri2numpy(m)
	subset0.append(mat)

print "Calculating..."
calculate(subset0, w0, w1, w2, sub)	
print "end\n"

print "Subset 1"
for index, file in enumerate(files[3:6]):
	sub = 1
	m = r("readRDS('"+ str(file)+"')")
	mat = rpyn.ri2numpy(m)
	subset1.append(mat)

print "Calculating..."
calculate(subset1, w0, w1, w2, sub)	
print "end\n"

print "Subset 2"
for index, file in enumerate(files[6:9]):
	sub = 2
	m = r("readRDS('"+ str(file)+"')")
	mat = rpyn.ri2numpy(m)
	subset2.append(mat)

print "Calculating..."
calculate(subset2, w0, w1, w2, sub)	
print "end"
