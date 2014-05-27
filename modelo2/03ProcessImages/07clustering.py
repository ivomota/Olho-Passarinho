import os
# from libraries import imtools
# from pylab import *

# def get_folder_clusters(path_folders):
# 	return [os.path.join(path_folders,f) for f in os.listdir(path_folders) if not f.endswith('.DS_Store')]

def get_clusters(path):
	return [os.path.join(path,f) for f in os.listdir(path)]

scripts = ['clustering0.R', 'clustering1.R', 'clustering2.R']

for script in scripts:
	cmmd = str("Rscript ../R_server/" + script)
	print cmmd
	os.system(cmmd)



# path_folders = '../R_server/clusters'
# folders = get_folder_clusters(path_folders)
# print folders

# content = []

# path = '../R_server/clusters'
# clusters = get_clusters(path)
# print clusters


###################

# f = open('R_server/clusters')
# for line in f:
#     content.append( line )
# f.close()

# # print content
# content = content[0].rstrip('\n')
# list = content.split(' ')

# vetor = map(int, list)
# maxim =  max(vetor)

# for i in range(0,maxim+1):
#  	clusters.append([item for item in range(len(vetor)) if vetor[item] == i])

# # get list of images
# imlist = imtools.get_imlist('../img/img_test/') 
# nbr_images = len(imlist)

# nr_cluster = len(clusters)
# print nr_cluster
# i = 0
# for cluster in clusters:
# 	l = len(cluster)
# 	i += 1
# 	print "Cluster" + str(i)
# 	for j in range(l):
# 		print imlist[cluster[j]]

# 	print " "


		
