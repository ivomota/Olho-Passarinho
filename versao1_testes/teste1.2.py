# -*- encoding: utf-8 -*-

import cStringIO # *much* faster than StringIO 
import cv2
import numpy as np
import imtools
import matplotlib.pyplot as plt
import cPickle as pickle

import vocabulary #Adicionado para teste

from PIL import Image
from scipy.cluster.vq import *

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
imlist = imtools.get_imlist('../img/sunsets/') 

imnbr = len(imlist)


# create matrix to store all flattened images
#immatrix = np.array([np.array(Image.open(im)) for im in imlist], dtype=object)


#Retrieve Keypoint Features 
keypoints_database = pickle.load( open( "keypoints_database.p", "rb" ) ) 

numkey = len(keypoints_database)
#print numkey

keypoints = [] 
descriptors = []

for i in range(numkey):
	keypoints, descriptor = unpickle_keypoints(keypoints_database[i])
	

	
	
'''	
# k-means
projected = whiten(descriptor)

#print len(projected)
centroids, distortion = kmeans(projected, 2)
code, distance = vq(projected, centroids)

features = projected



plt.figure()
ndx = np.where(code==0)[0] 
plt.plot(features[ndx,0],features[ndx,1],'*') 
ndx = np.where(code==1)[0] 
plt.plot(features[ndx,0],features[ndx,1],'r.') 
plt.plot(centroids[:,0],centroids[:,1],'go') 
plt.axis('off')
plt.show()
'''


'''
	for point in keypoints:
		print 'x = ' + str(point.pt[0]) + '; y = ' + str(point.pt[1])

'''

