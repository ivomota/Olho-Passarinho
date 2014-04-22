import pickle 
import vocabulary
import imtools
import sift


# get list of images
imlist = imtools.get_imlist('./img/') 
nbr_images = len(imlist)
featlist = [ imlist[i][:-3]+'sift' for i in range(nbr_images) ]

#create vocabulary
voc = vocabulary.Vocabulary('vocab')
voc.train(featlist,1000,10)

# saving vocabulary
with open('vocabulary.pkl', 'wb') as f:
  pickle.dump(voc,f)
print 'vocabulary is:', voc.name, voc.nbr_words
