# -*- encoding: utf-8 -*-

import cStringIO # *much* faster than StringIO 
import cv2
import numpy as np
import imtools
import matplotlib.pyplot as plt

from scipy.cluster.vq import *

def write_features_to_file(filename,locs,desc):
	""" Save feature location and descriptor to file. """ 
	savetxt(filename,hstack((locs,desc)))


# get list of images
imlist = imtools.get_imlist('../img/sunsets/teste/') 

imnbr = len(imlist)

f = open('./features.txt', 'w')

plt.figure()


for i in range(imnbr):
	# read image
	im = cv2.imread(imlist[i])

	# down sample
	im_lowres = cv2.pyrDown(im)

	# convert to grayscale
	gray = cv2.cvtColor(im_lowres,cv2.COLOR_RGB2GRAY)

	# detect feature points
	s = cv2.SIFT()
	mask = np.uint8(np.ones(gray.shape))
	keypoints = s.detect(gray,mask)

	f.write(str(keypoints[::10])+'\n')

	# show image and points
	vis = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)
	for k in keypoints[::10]: 
		cv2.circle(vis,(int(k.pt[0]),int(k.pt[1])),2,(0,255,0),-1) 
		cv2.circle(vis,(int(k.pt[0]),int(k.pt[1])),int(k.size),(0,255,0),2)
		
		
	#cv2.imshow('local descriptors',vis)
	#cv2.waitKey()
	
	plt.subplot(1,3,i+1)
	plt.imshow(vis) 
	plt.axis('off')

plt.show()





