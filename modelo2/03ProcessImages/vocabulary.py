from numpy import *
from scipy.cluster.vq import *
import sift
import sys


class Vocabulary(object):
    
    def __init__(self,name):
        self.name = name
        self.voc = []
        self.idf = []
        self.trainingdata = []
        self.nbr_words = 0

        self.error = []
    
    def train(self,featurefiles,k=100,subsampling=10):
        """ Train a vocabulary from features in files listed 
            in featurefiles using k-means with k number of words. 
            Subsampling of training data can be used for speedup. """
        
        nbr_images = len(featurefiles)
        print "Number of images: ", nbr_images
        # read the features from file
        descr = []
        descr.append(sift.read_features_from_file(featurefiles[0])[1])
        descriptors = descr[0] #stack all features for k-means
	   
        error = []

        print "Geting all features..."
        end_val = nbr_images
        for i in arange(1,nbr_images):
            try:
                descr.append(sift.read_features_from_file(featurefiles[i])[1])
                descriptors = vstack((descriptors,descr[i]))
            except:
                self.error.append(featurefiles[i])
            
            percent = float(i) / end_val
            bar_length = 20
            hashes = '=' * int(round(percent * bar_length))
            spaces = ' ' * (bar_length - len(hashes))
            sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
            sys.stdout.flush()
         
        print "\nKmeans clustering for visual words"
        # k-means: last number determines number of runs
        self.voc,distortion = kmeans(descriptors[::subsampling,:],k,1)
        self.nbr_words = self.voc.shape[0]
        
        print "\nProjecting on vocabulary"   
        # go through all training images and project on vocabulary
        imwords = zeros((nbr_images,self.nbr_words))
        for i in range( nbr_images ):
            imwords[i] = self.project(descr[i])
        
        print "\nFinishing..."
        nbr_occurences = sum( (imwords > 0)*1 ,axis=0)
        
        self.idf = log( (1.0*nbr_images) / (1.0*nbr_occurences+1) )
        self.trainingdata = featurefiles

    
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
