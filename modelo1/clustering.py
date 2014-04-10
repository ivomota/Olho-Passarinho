import os
import imtools
from pylab import *

cmmd = str("Rscript R_Project_server/clustering.R")
print cmmd
os.system(cmmd)

content = []
clusters = []

f = open('ctest.txt')
for line in f:
    content.append( line )
f.close()

# print content
content = content[0].rstrip('\n')
list = content.split(' ')

vetor = map(int, list)
maxim =  max(vetor)

for i in range(0,maxim+1):
 	clusters.append([item for item in range(len(vetor)) if vetor[item] == i])

# get list of images
imlist = imtools.get_imlist('../img/img_test/') 
nbr_images = len(imlist)

nr_cluster = len(clusters)
print nr_cluster
i = 0
for cluster in clusters:
	l = len(cluster)
	i += 1
	print "Cluster" + str(i)
	for j in range(l):
		print imlist[cluster[j]]

	print " "


		
