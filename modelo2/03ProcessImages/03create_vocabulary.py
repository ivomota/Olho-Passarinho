import pickle

from libraries import vocabulary
from libraries import imtools
from libraries import sift


# get list of images
imlist = imtools.get_imlist('./img/') 
nbr_images = len(imlist)
featlist = [ imlist[i][:-4]+'sift' for i in range(nbr_images) ]


#create vocabulary
voc = vocabulary.Vocabulary('vocab')
voc.train(featlist[0:450],1000,100)
print 'vocabulary errors: ' + str(len(voc.error))

#saving vocabulary
with open('vocabulary.pkl', 'wb') as f:
  pickle.dump(voc,f)
print 'vocabulary is:', voc.name, voc.nbr_words

data = load('../tweets_instagram_final.pkl')
length = len(data)

w = open('im_to_rm.txt', 'w')
w.write(str(voc.error))
w.close()

