# -*- encoding: utf-8 -*-

import cStringIO # *much* faster than StringIO 
import matplotlib.pyplot as plt

import imtools		#ficheiro
import vocabulary 	#ficheiro
import sift		#ficheiro

from PIL import Image


# get list of images
imlist = imtools.get_imlist('../img/sunsets/treino') 


nbr_images = len(imlist)

featlist = [ imlist[i][:-3]+'sift' for i in range(nbr_images)]


voc = vocabulary.Vocabulary('test')
voc.train(featlist,1000,10)
# saving vocabulary
#with open('vocabulary.pkl', 'wb') as f:
  #pickle.dump(voc,f)
#print 'vocabulary is:', voc.name, voc.nbr_words
