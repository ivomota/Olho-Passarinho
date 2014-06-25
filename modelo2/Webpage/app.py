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

@app.route('/')
def start():
	return render_template('app.html')

@app.route('/subset', methods= ['GET', 'POST'])
def cluster():
	req = request.form['subset']
	pimg = request.form['pesoimg']
	pesp = request.form['pesoesp']
	ptmp = request.form['pesotemp']

	print pimg, pesp, ptmp

	if req == "null":
		return render_template('test.html')
	else:
		path = 'static/clusters/' + str(req)
		folders = get_clusters(path)
		# print folders

		clusters = []
		for folder in folders:
			# if folder == "static/clusters/"+ str(req) +"/c_0.5_0.25_0.25":
			if folder == "static/clusters/"+ str(req) +'/c_'+str(pimg)+'_'+str(pesp)+'_'+str(ptmp):
				clusters = get_clusters(folder)
				print folder

		# Create dictionary with name of cluster and index of tweet
		dic = {}
		for index, cluster in enumerate(clusters):
			numbers = read_files(cluster)
			lst = [int(k) for k in numbers.split(' ')]
			lst = [l-1 for l in lst]
			dic['cluster' + str(index)] = lst
		#print dic

		#Create a list with the name of clusters
		clusters = []
		for key, value in dic.iteritems():
			clusters.append(key)
		clusters.sort()
		
		# return "Boa"		
		# return render_template('app.html', clusters =  c, files = jfile, geoinfo = dic2)
		subset = req[1]
		return render_template('app.html', jsonfile = subset, clusters = clusters)


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')