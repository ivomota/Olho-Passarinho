
import numpy as np
import pickle as p
import matplotlib.pyplot as plt
import imtools
import pca

from pylab import *
from scipy.cluster.vq import *
from StringIO import StringIO   # StringIO behaves like a file object
from PIL import Image


if __name__ == '__main__':
	# get list of images
	imlist = imtools.get_imlist('../img/teste/') 

	imnbr = len(imlist)
	
	print imnbr

	# create matrix to store all flattened images
	immatrix = np.array([np.array(Image.open(im)).flatten() for im in imlist], 'f')

	V, S, immean = pca.pca(immatrix)


	# project on the 40 first PCs
	immean = immean.flatten()
	projected = np.array([np.dot(V[:40], immatrix[i]-immean) for i in range(imnbr)])

	# k-means
	projected = whiten(projected)
	centroids, distortion = kmeans(projected, 4)
	code, distance = vq(projected, centroids)

	# plot clusters
	for k in range(4):
		ind = np.where(code==k)[0]
		plt.figure()
		plt.gray()
		for i in range(np.minimum(len(ind),40)):
			plt.subplot(4,10,i+1) 
			plt.imshow(immatrix[ind[i]].reshape((128,128))) 
			plt.axis('off')
	plt.show()

