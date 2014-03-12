import pickle 
import sift
import imagesearch
import imtools


# get list of images
imlist = imtools.get_imlist('../img/sunsets/treino/') 
nbr_images = len(imlist)
featlist = [ imlist[i][:-3]+'sift' for i in range(nbr_images) ]

# load vocabulary
with open('vocabulary.pkl', 'rb') as f:
  voc = pickle.load(f)

# create indexer
indx = imagesearch.Indexer('test.db',voc)
indx.create_tables()

# go through all images, project features on vocabulary and insert
for i in range(nbr_images)[:100]:
	locs,descr = sift.read_features_from_file(featlist[i]) 
	indx.add_to_index(imlist[i],descr)

# commit to database
indx.db_commit()
