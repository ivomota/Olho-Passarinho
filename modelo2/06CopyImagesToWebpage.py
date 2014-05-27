import os
import shutil

def get_files(path):
	return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpeg')]

path = './03ProcessImages/img/'
imfiles = get_files(path)

path_dst = './07Webpage/static/img/'

for imfile in imfiles:
	name = imfile.split('/')[3]
	# print name
	dst = path_dst + name
	if not os.path.isfile(dst):
		shutil.copyfile(imfile, dst)
