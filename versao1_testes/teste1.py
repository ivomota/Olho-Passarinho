# -*- encoding: utf-8 -*-

import cStringIO # *much* faster than StringIO 
import cv2
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle

import imtools		#ficheiro

from scipy.cluster.vq import *

def pickle_keypoints(keypoints, descriptors): 
	i = 0 
	temp_array = [] 
	for point in keypoints: 
		temp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id, descriptors[i]) 
		i+=1 
		temp_array.append(temp) 
	return temp_array


# get list of images
imlist = imtools.get_imlist('../img/sunsets/treino/') 

imnbr = len(imlist)


dic = 100

temp_array = [] 

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
	keypoints, descriptor = s.detectAndCompute(gray,mask)
	
	#Store and Retrieve keypoint features 
	temp = pickle_keypoints(keypoints, descriptor) 
	temp_array.append(temp)

	image =  imlist[i][:-3]
	pickle.dump(temp_array, open(str(image)+"sift", "wb"))




