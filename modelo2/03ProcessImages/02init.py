import imtools
import sift

import sys
import os


def get_siftlist(path):
    """    Returns a list of filenames for 
        all jpg images in a directory. """
        
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.sift')]

path = './img/'

# get list of images
imlist = imtools.get_imlist(path) 
nbr_images = len(imlist)
print "Numero de imagens armazenadas: " + str(nbr_images)


featlist = [ imlist[i][:-4]+'sift' for i in range(nbr_images)]

exist_sift = get_siftlist(path)
nr_exist = len(exist_sift)

end_val = nbr_images
for i in range(nbr_images): # [nr_exist:end_val]:
	if not featlist[i] in exist_sift:
		sift.process_image(imlist[i],featlist[i])

		percent = float(i) / end_val
		bar_length = 20
		hashes = '=' * int(round(percent * bar_length))
		spaces = ' ' * (bar_length - len(hashes))
		sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
		sys.stdout.flush()

