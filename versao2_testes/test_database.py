#first teste
import sqlite3 as sqlite

#secound teste
import imagesearch
import sift
import imtools
import vocabulary as voc

#con = sqlite.connect('test.db')
#print con.execute('select count (filename) from imlist').fetchone() 
#print con.execute('select * from imlist').fetchone() 


# get list of images
imlist = imtools.get_imlist('../img/sunsets/treino/') 
image = '../img/sunsets/treino/3486007526_713e52862e.jpg'
nbr_images = len(imlist)
featlist = [ imlist[i][:-3]+'sift' for i in range(nbr_images) ]

src = imagesearch.Searcher('test.db', 'vocabulary.plk')

#imagesearch.compute_ukbench_score(src,imlist)


nbr_results = 6
res = [w[1] for w in src.query(image)[:nbr_results]] 
imagesearch.plot_results(src,res)


#print 'try a query...'
#print src.query(imlist[0])[:10]

