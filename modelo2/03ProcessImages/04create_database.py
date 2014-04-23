import pickle 
import sift
import imagesearch
import imtools


# get list of images
imlist = imtools.get_imlist('./img/') 
nbr_images = len(imlist)
featlist = [ imlist[i][:-4]+'sift' for i in range(nbr_images) ]

# load vocabulary
with open('vocabulary.pkl', 'rb') as f:
  voc = pickle.load(f)

# create indexer
indx = imagesearch.Indexer('vocab.db',voc)
indx.create_tables()

# go through all images, project features on vocabulary and insert
for i in range(nbr_images):
	locs,descr = sift.read_features_from_file(featlist[i]) 
	indx.add_to_index(imlist[i],descr)

# commit to database
indx.db_commit()
