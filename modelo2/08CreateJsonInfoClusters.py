import json
from bson import json_util
import os
from numpy import *
import pickle
import math

## Temporary
from datetime import datetime
from dateutil import parser
##

def get_clusters(path):
    """    Returns a list of folders for 
        all clusters images in a directory. """ 
    return [os.path.join(path,f) for f in os.listdir(path) if not f.endswith('.DS_Store')]

def read_files(path):
	f = open(path, 'r')
	info = f.read()
	f.close()
	return info

def load_all_data(filename):
	path = './Webpage/static/data/' + str(filename)
	# print path
	# load file
	with open(path) as json_data:
		d = json.load(json_data)
		json_data.close()
	return d

def load_spatial_matrix(subset):
	subset = subset[1]
	filename = './04SpatioTemporal/matrix_spatial/matrix' + str(subset) + '_non_normalized.pkl'
	# Open file
	pkl_file = open(filename, 'rb')
	# Load from Pickle file.
	data = pickle.load(pkl_file)
	pkl_file.close()
	return data

def write_file(data, filename):
	path = './Webpage/static/temp/' + str(filename) +'.json'
	s = json_util.dumps(data, default=json_util.default)
	f = open(path, 'w')
	f.write(str(s))
	f.close()

def sort_by_creation(d):
    '''a helper function for sorting'''
    return d['created_at']


#Start Script
subsets = ['S0', 'S1', 'S2']

for sub in subsets:
	path = './Webpage/static/clusters/' + str(sub)
	folders = get_clusters(path)

	#get matrix spatial distances and transport
	spatial_data = load_spatial_matrix(sub)
	transp = spatial_data.T
	l = len(spatial_data)
	x1 = spatial_data.reshape((l,l))
	x2 = transp.reshape((l,l))
	spatial_mat = add(x1, x2)

	# print folders
	clusters = []
	for folder in folders:
		if folder == "./Webpage/static/clusters/"+ str(sub)+"/c_0.5_0.25_0.25":
			clusters = get_clusters(folder)

	# Create dictionary with name of cluster and index of tweet
	dic = {}

	for index, cluster in enumerate(clusters):
		numbers = read_files(cluster)
		lst = [int(k) for k in numbers.split(' ')]
		lst = [l-1 for l in lst]
		dic['cluster' + str(index)] = lst
	# print dic.keys()

	# Load json file 
	filename = str(sub)+'.json'
	print "Ficheiro json carregado:", filename
	json_d = load_all_data(filename)

	# Calc geo center of a cluster
	# Create a dictionary with name of cluster and the index of centroid and the radius
	dic2 = {}
	for cname, indx_list in dic.iteritems():
		minm = 0
		center_index = 0
		radius = 0
		count = 0
		# print cname
		for w1 in indx_list:
			count += 1
			dist = 0
			d = []
			
			d = [p for indx, p in enumerate(spatial_mat[w1]) if indx in indx_list and indx != w1 ]
			dist = sum(d)

			if dist < minm or count == 1:
				minm = dist
				center_index = w1
				radius = max(d)
				# print "O novo valor minimo e: ", minm

		if radius == 0:
			radius = 100
		print "O raio e: ", radius

		data_c = [j for ind, j in enumerate(json_d) if ind in indx_list]
		
		print data_c[0]['created_at']
		sorted_data = sorted(data_c, key=sort_by_creation)
		print sorted_data[0]['created_at']



		start_date = sorted_data[0]['created_at']
		end_date = sorted_data[-1]['created_at']

		dic2[cname] = {"center_index": str(center_index), "radius":str(radius), "start_date": start_date, "end_date": end_date}
	# print dic2

	#Create a json file with theinformation of the name of cluster and index-1
	write_file(dic, "clusters_elements_"+str(sub))
	write_file(dic2, "clusters_info_"+str(sub))