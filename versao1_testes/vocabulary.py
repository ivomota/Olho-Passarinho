from numpy import *
from scipy.cluster.vq import *
import cPickle as pickle
import cv2
import numpy as np

class Vocabulary(object):
    
    def __init__(self,name):
        self.name = name
        self.voc = []
        self.idf = []
        self.trainingdata = []
        self.nbr_words = 0
    
    def train(self,featurefiles,k=100,subsampling=10):
        """ Train a vocabulary from features in files listed 
            in featurefiles using k-means with k number of words. 
            Subsampling of training data can be used for speedup. """
        
	def unpickle_keypoints(array): 
		keypoints = [] 
		descriptors = [] 
		for point in array: 
			temp_feature = cv2.KeyPoint(x=point[0][0],y=point[0][1],_size=point[1], _angle=point[2], _response=point[3], _octave=point[4], _class_id=point[5]) 
			temp_descriptor = point[6] 
			keypoints.append(temp_feature) 
			descriptors.append(temp_descriptor) 
		return keypoints, np.array(descriptors)

        nbr_images = len(featurefiles)
	
	key = [] 
	desc = []
	
	k = []
	d = []

	descr = []
	keypoints_database = []

	#Retrieve Keypoint Features 
	for j in range(nbr_images):
		keypoints_database = pickle.load( open( str(featurefiles[j] ), "rb" ) )

		numkey = len(keypoints_database)

		for i in range(numkey):
			key, des = unpickle_keypoints(keypoints_database[i])
		
		k.append(key)
		d.append(des)
	
	print len(d)
			
	descr.append(d[0])
	
	
	print len(descr)
	

	'''
        # read the features from file
        descr = []
	
	
        descr.append(sift.read_features_from_file(featurefiles[0])[1])
        descriptors = descr[0] #stack all features for k-means
        for i in arange(1,nbr_images):
            descr.append(sift.read_features_from_file(featurefiles[i])[1])
            descriptors = vstack((descriptors,descr[i]))
        '''   
        # k-means: last number determines number of runs
        #self.voc,distortion = kmeans(descriptors[::subsampling,:],k,1)
        #self.nbr_words = self.voc.shape[0]
        
        # go through all training images and project on vocabulary
        #imwords = zeros((nbr_images,self.nbr_words))
	#print imwords[1]
        #for i in range( nbr_images ):
            #imwords[i] = self.project(descr[i])
        '''
        nbr_occurences = sum( (imwords > 0)*1 ,axis=0)
        
        self.idf = log( (1.0*nbr_images) / (1.0*nbr_occurences+1) )
        self.trainingdata = featurefiles
    	'''

    def project(self,descriptors):
        """ Project descriptors on the vocabulary
            to create a histogram of words. """
        
        # histogram of image words 
        imhist = zeros((self.nbr_words))
        words,distance = vq(descriptors,self.voc)
        for w in words:
            imhist[w] += 1
        
        return imhist
    
    def get_words(self,descriptors):
        """ Convert descriptors to words. """
        return vq(descriptors,self.voc)[0]
