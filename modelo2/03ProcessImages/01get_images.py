# -*- encoding: utf-8 -*-
import cStringIO # *much* faster than StringIO
import urllib
import urllib2
import sys
from PIL import Image

import pickle


def load(filename, verbose=False):
    # Open file
    if verbose : print("Loading %s" % filename)
    pkl_file = open(filename, 'rb')
    # Load from Pickle file.
    data = pickle.load(pkl_file)
    pkl_file.close()
    return data

def get(qry):
	end_val = len(qry)
	i=0
	j=0
	failed = 0
	nofound = 0
	toremove = []
	# print qry
	for URL in qry:
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
			toremove.append(j)

		if deadLinkFound == False:
			try:
				file1 = urllib.urlopen(full_url)
				im = cStringIO.StringIO(file1.read())  # constructs a StringIO holding the image
				img = Image.open(im)

				# now use PIL
				# print img.format, img.size, img.mode
				form = str(img.format)
				format = form.lower()
				image_to_save = './img/'+ str(i)+ '_' + str(id_tweet) +'.'+ format
				img.save(image_to_save)
				i+=1
			except:
				toremove.append(j)
				failed += 1
				# print "Image nr " +  str(j) + " download failed\n"
		j+=1
		percent = float(j) / end_val
		# sys.stdout.write("\r%d%%" %progress)
		# sys.stdout.write('\r[{0}] {1}%'.format('#'*(progress/10), progress))
		bar_length = 20
		hashes = '=' * int(round(percent * bar_length))
		spaces = ' ' * (bar_length - len(hashes))
		sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
		sys.stdout.flush()
	print "Numero total de imagens: " + str(j)	
	print "Numero total de imagens guardadas: " + str(i)
	print "Numero total de imagens não encontradas: " + str(i)
	print "Numero total de imagens falharam o download: " + str(failed)
	print "Numero total de tweets para remover: " + str(len(toremove))
	return toremove


data = load('../tweets_instagram.pkl')
length = len(data)
print length

qry = []

for i in xrange(length):
	img = []
	img.append(data[i]['entities']['urls'][0]['display_url'])
	img.append(data[i]['id_str'])
	qry.append(img)

# print qry[173]

rmv = get(qry)
for k in rmv:
	del data[k]

print "\n"
print "Total numero de tweets com imagems: " + str(len(data))

saving
with open('../tweets_instagram_final.pkl', 'wb') as f:
  pickle.dump(data,f)

