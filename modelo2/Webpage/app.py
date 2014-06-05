from flask import Flask, request, render_template, url_for
import os
import json
from bson import json_util
import math
from numpy import *
import pickle



app = Flask(__name__)

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
	path = './static/data/' + str(filename)
	# print path
	# load file
	with open(path) as json_data:
		d = json.load(json_data)
		json_data.close()
	return d

def write_file(data, filename):
	path = './static/temp/' + str(filename) +'.json'
	s = json_util.dumps(data, default=json_util.default)
	f = open(path, 'w')
	f.write(str(s))
	f.close()

def load_cluster_data(path):
	with open(path) as json_data:
		cdata = json.load(json_data)
		json_data.close()
	return cdata

def load_spatial_matrix(subset):
	subset = subset[1]
	filename = '../04SpatioTemporal/matrix_spatial/matrix' + str(subset) + '_non_normalized.pkl'
	# Open file
	pkl_file = open(filename, 'rb')
	# Load from Pickle file.
	data = pickle.load(pkl_file)
	pkl_file.close()
	return data

@app.route('/')
def start():
	return render_template('app.html')

@app.route('/subset', methods= ['GET', 'POST'])
def cluster():
	req = request.form['subset']
	if req == "null":
		return render_template('test.html')
	else:
		path = 'static/clusters/' + str(req)
		folders = get_clusters(path)
		# print folders

		#get matrix spatial distances and transport
		spatial_data = load_spatial_matrix(req)
		transp = spatial_data.T
		l = len(spatial_data)
		x1 = spatial_data.reshape((l,l))
		x2 = transp.reshape((l,l))
		spatial_mat = add(x1, x2)

		clusters = []
		for folder in folders:
			if folder == "static/clusters/"+ str(req) +"/c_0.5_0.25_0.25":
				clusters = get_clusters(folder)
		
		# Create dictionary with name of cluster and index of tweet
		dic = {}
		for index, cluster in enumerate(clusters):
			numbers = read_files(cluster)
			lst = [int(k) for k in numbers.split(' ')]
			lst = [l-1 for l in lst]
			dic['cluster' + str(index)] = lst
		#print dic

		# Load json file 
		filename = str(req) + '.json'
		print "Ficheiro json carregado:", filename
		json = load_all_data(filename)


		# Calc geo center of a cluster
		# Create a dictionary with name of cluster and the index of centroid and the radius
		dic2 = {}
		for cname, indx_list in dic.iteritems():
			minm = 0
			center_index = 0
			radius = 0
			count = 0
			print cname
			# indx_list = [i-1 for i in indx_list]
			# print indx_list
			for w1 in indx_list:
				count += 1
				dist = 0
				
				d = [p for indx, p in enumerate(spatial_mat[w1]) if indx in indx_list and indx != w1 ]
				# d = [p for p in spatial_mat[w1]]

				dist = sum(d)

				if dist < minm or count == 1:
					minm = dist
					center_index = w1 - 1
					radius = max(d)
					# print "O novo valor minimo e: ", minm

			if radius == 0:
				radius = 10
			print "O raio e: ", radius

			dic2[str(cname)] = [center_index, radius]
		# print dic2

		#Create a json file with theinformation of the name of cluster and index-1
		write_file(dic, "clusters_info")

		#Create a list with the name of clusters
		clusters = []
		for key, value in dic.iteritems():
			clusters.append(key)
		clusters.sort()

		# Create json file only with tweets from cluster
		# for key, value in dic.iteritems():
			# data = [json[i-1] for i in value]
			# print str(key) + ': ' + str(len(data))
			# print data[0]
			# write_file(data, key)

		# Get data
		# json_path = './static/temp/'
		# jfile = get_clusters(json_path)
		# c = [name.split('/')[3].split('.')[0] for name in jfile ]
		

		# return "Boa"		
		# return render_template('app.html', clusters =  c, files = jfile, geoinfo = dic2)
		subset = req[1]
		return render_template('app.html', jsonfile = subset, geoinfo = dic2, clusters = clusters)


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')