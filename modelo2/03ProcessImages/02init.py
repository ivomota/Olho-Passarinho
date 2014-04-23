import imtools
import sift

import pickle

# def load(filename, verbose=False):
#     # Open file
#     if verbose : print("Loading %s" % filename)
#     pkl_file = open(filename, 'rb')
#     # Load from Pickle file.
#     data = pickle.load(pkl_file)
#     pkl_file.close()
#     return data


# #Start
# data = load('../tweets_instagram_final.pkl')
# length = len(data)
# print "Numero de imagens guardadas: " + str(length)


# get list of images
imlist = imtools.get_imlist('./img/') 
nbr_images = len(imlist)
print "Numero de imagens guardadas: " + str(nbr_images)


featlist = [ imlist[i][:-3]+'sift' for i in range(nbr_images)]

for i in range(nbr_images): 
	sift.process_image(imlist[i],featlist[i])
