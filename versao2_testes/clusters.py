import imagesearch
import pickle 
import sift
import imtools
import vocabulary as voc

# import PIL and pylab for plotting        
from PIL import Image
from scipy.cluster.vq import *
from numpy import *
from pylab import *

#Teste de apresentacao de varios clusters


# get list of images
imlist = imtools.get_imlist('../img/sunsets/treino/')
nbr_images = len(imlist)
featurefiles = [ imlist[i][:-3]+'sift' for i in range(nbr_images) ]


nbr_results = 6

for i in range(2):
	image = imlist[i]
	res = [w[1] for w in src.query(image)[:nbr_results]] 
	imagesearch.plot_results(src,res)