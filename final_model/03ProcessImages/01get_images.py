# -*- encoding: utf-8 -*-
import cStringIO # *much* faster than StringIO
import urllib
import urllib2
import sys
from PIL import Image

import pickle
# import imtools
from libraries import imtools

def load(filename, verbose=False):
    # Open file
    if verbose : print("Loading %s" % filename)
    pkl_file = open(filename, 'rb')
    # Load from Pickle file.
    data = pickle.load(pkl_file)
    pkl_file.close()
    return data

def get(qry, saved):
	end_val = len(qry)
	i=0
	j=0
	failed = 0
	nofound = 0
	toremove = []
	# print qry
	count = 0
	for URL in qry:
		j+=1

		if not URL[1] in saved:

			n = URL[0].split('/')

			if str(n[0]) == 'twitpic.com':
				n = str(n[1]) 
				full_url = ('http://twitpic.com/show/full/' + n )
			elif str(n[0]) == 'instagram.com':
				url_inst = str(URL[0]) 
				full_url = 'http://'+url_inst+'media/?size=l\n'
			elif str(n[0]) == 'pic.twitter.com':
				print str(URL[0])	
			id_tweet = URL[1]
			try:
				p = urllib2.urlopen(urllib2.Request(full_url))
			  	deadLinkFound = False
				# print "Image nr " +  str(j)
			  	# print full_url
			except:
				deadLinkFound = True
				# print "Image nr " +  str(j) + " not found\n"
				nofound += 1
				toremove.append(j-1)

			if deadLinkFound == False:
				try:
					file1 = urllib.urlopen(full_url)
					im = cStringIO.StringIO(file1.read())  # constructs a StringIO holding the image
					img = Image.open(im)

					# now use PIL
					# print img.format, img.size, img.mode
					form = str(img.format)
					format = form.lower()
					# image_to_save = './img/'+ str(i)+ '_' + str(id_tweet) +'.'+ format
					image_to_save = './img/'+ str(id_tweet) +'.'+ format
					img.save(image_to_save)
					i+=1
				except:
					toremove.append(j-1)
					failed += 1
					# print "Image nr " +  str(j) + " download failed\n"
			# j+=1
			percent = float(j) / end_val
			bar_length = 20
			hashes = '=' * int(round(percent * bar_length))
			spaces = ' ' * (bar_length - len(hashes))
			sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
			sys.stdout.flush()
	print '\n'
	print "Numero total de imagens: " + str((j))	
	print "Numero total de imagens guardadas: " + str(i)
	print "Numero total de imagens não encontradas: " + str(nofound)
	print "Numero total de imagens falharam o download: " + str(failed)
	print "Numero total de tweets para remover: " + str(len(toremove))
	return toremove


#Start
data = load('../tweets_instagram.pkl')
length = len(data)
print "Numero de imagens para guaradar: " + str(length)

# get list of images
imlist = imtools.get_imlist('./img/') 
nr_images = len(imlist)
print "Numero de imagens já guardadas: " + str(nr_images)
print "\n"

saved = []

if nr_images > 0:
	for im in imlist:
		a = im.split('/')
		b = a[2].split('.')[0]
		# c = b.split('_')[1]
		# saved.append(c)
		saved.append(b)


qry = []

for i in xrange(length):
	img = []
	img.append(data[i]['entities']['urls'][0]['display_url'])
	img.append(data[i]['id_str'])
	qry.append(img)

#download images
to_delete = get(qry, saved)
nr_to_delete = len(to_delete)
print nr_to_delete


r = open('../tweets_to_delete.txt', 'w')
r.write(str(to_delete))
r.close()

#remove duplicates
if nr_to_delete > 0:
	for offset, index in enumerate(to_delete):
		index -= offset
		del data[index]

print "\n"
print "Total numero de tweets com imagems após limpeza: " + str(len(data))

# saving
with open('../tweets_instagram_final.pkl', 'wb') as f:
  pickle.dump(data,f)

'''
Percent: [====================] 100 
Numero total de imagens: 7195
Numero total de imagens guardadas: 5958
Numero total de imagens não encontradas: 5958
Numero total de imagens falharam o download: 7
Numero total de tweets para remover: 1237
Traceback (most recent call last):
  File "01get_images.py", line 99, in <module>
    del data[k]
IndexError: list assignment index out of range

'''
