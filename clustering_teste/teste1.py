# -*- encoding: utf-8 -*-

import cStringIO # *much* faster than StringIO 
import cv2
import numpy as np
import imtools
import matplotlib.pyplot as plt
import cPickle as pickle

from scipy.cluster.vq import *

def pickle_keypoints(keypoints, descriptors): 
	i = 0 
	temp_array = [] 
	for point in keypoints: 
		temp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id, descriptors[i]) 
		i+=1 
		temp_array.append(temp) 
	return temp_array


def unpickle_keypoints(array): 
	keypoints = [] 
	descriptors = [] 
	for point in array: 
		temp_feature = cv2.KeyPoint(x=point[0][0],y=point[0][1],_size=point[1], _angle=point[2], _response=point[3], _octave=point[4], _class_id=point[5]) 
		temp_descriptor = point[6] 
		keypoints.append(temp_feature) 
		descriptors.append(temp_descriptor) 
	return keypoints, np.array(descriptors)


# get list of images
imlist = imtools.get_imlist('../img/sunsets/teste/') 

imnbr = len(imlist)

print imnbr

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


pickle.dump(temp_array, open("keypoints_database.p", "wb"))




