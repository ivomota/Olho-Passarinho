# -*- encoding: utf-8 -*-
import cStringIO # *much* faster than StringIO
import urllib
import urllib2
import sys
from PIL import Image
# import sqlite3


# location = 'data.db'
# table_name = 'imagens'
# qry = "SELECT url, id_objeto FROM imagens WHERE tipo = 'Tweet' LIMIT 100;"

# conn = sqlite3.connect(location)
# c = conn.cursor()

# for URL in c.execute(qry):


def get(qry):
	i=0
	j=0
	# print qry
	for URL in qry:
		n = URL[0].split('/') 
		n = str(n[1]) 
		full_url = ('http://twitpic.com/show/full/' + n )
		j+=1
		id_tweet = URL[1]
		try:
		  p = urllib2.urlopen(urllib2.Request(full_url))
		  deadLinkFound = False
		  print full_url
		except:
		  deadLinkFound = True

		if deadLinkFound == False:
			file1 = urllib.urlopen(full_url)
			im = cStringIO.StringIO(file1.read())  # constructs a StringIO holding the image
			img = Image.open(im)

			# now use PIL
			print img.format, img.size, img.mode
			format = img.format
			image_to_save = './img/'+ str(id_tweet) +'.'+ str(format)
			img.save(image_to_save)
			i+=1
	print "Numero total de imagens: " + str(j)	
	print "Numero total de imagens guardadas: " + str(i)
# conn.commit()
# c.close()
# conn.close()




	
#URL para intagram
# url_inst = data[i]["entities"]["urls"][0]["expanded_url"]
# full_url_inst = url_inst+'media/?size=l\n'

# try:
#   p = urllib2.urlopen(urllib2.Request(full_url_inst))
#   deadLinkFound = False
# except:
#   deadLinkFound = True

# if deadLinkFound == False:
# 	file1 = urllib.urlopen(full_url_inst)
# 	im = cStringIO.StringIO(file1.read())  # constructs a StringIO holding the image
# 	img = Image.open(im)

# 	# now use PIL
# 	print img.format, img.size, img.mode
# 	format = img.format
# 	image_to_save = '/Applications/MAMP/htdocs/Tese/img/my_copy_'+ str(i) +'.'+ str(format)
# 	img.save(image_to_save)

