import imtools
import sift


# get list of images
imlist = imtools.get_imlist('./img/') 
nbr_images = len(imlist)

featlist = [ imlist[i][:-3]+'sift' for i in range(nbr_images)]

for i in range(nbr_images): 
	sift.process_image(imlist[i],featlist[i])
