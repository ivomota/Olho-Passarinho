from numpy import *
import os
import shutil

def get_cfiles(path):
	"""    Returns a list of folders for 
    all clusters images in a directory. """ 
	return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.txt')]

def getcluster(cfile):
	cluster = loadtxt(str(cfile), dtype=(str))
	return cluster

def im_urls(cluster):
	data = load('./tweets_instagram_final.pkl')
	urls = []
	for index in cluster:
		i = int(index)
		url = str(data[i-1]['id_str']) + '.jpeg'
		urls.append(url)
	return urls

path = './R_server/clusters/'
cfiles = get_cfiles(path)
print cfiles

for i, cfile in enumerate(cfiles):
	cluster = getcluster(cfile)
	images = im_urls(cluster)

	path_orig = './03ProcessImages/img/'
	path_dest = './06Webpage/static/img/C'+ str(i) +'/'

	if not os.path.exists(path_dest):
		os.makedirs(path_dest)

	# try:
	#     os.stat(path_dest)
	# except:
	#     os.mkdir(path_dest) 

	for image in images:
		src = path_orig + image
		dst = path_dest + image
		shutil.copyfile(src, dst)

