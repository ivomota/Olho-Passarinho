from flask import Flask, request, render_template, url_for
import os
import json
from bson import json_util

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

def load(filename):
	path = './static/data/' + str(filename)
	# print path
	# load file
	with open(path) as json_data:
		d = json.load(json_data)
		json_data.close()
	return d

def write_file(data, filename):
	path = './static/temp/' + str(filename) +'.json'
	s0 = json_util.dumps(data, default=json_util.default)
	f0 = open(path, 'w')
	f0.write(str(s0))
	f0.close()

@app.route('/')
def start():
	return render_template('app.html')

@app.route('/cluster', methods= ['GET', 'POST'])
def cluster():
	req = request.form['subset']
	if req == "null":
		return render_template('test.html')
	else:
		path = 'static/clusters/' + str(req)
		folders = get_clusters(path)
		# print folders
		
		clusters = []
		for folder in folders:
			if folder == "static/clusters/S0/c_0.5_0.25_0.25":
				clusters = get_clusters(folder)
		
		# Create dictionary with name of cluster and index of tweet
		dic = {}
		for index, cluster in enumerate(clusters):
			numbers = read_files(cluster)
			lst = [int(k) for k in numbers.split(' ')]
			dic['cluster' + str(index)] = lst
		
		# Load json file 
		filename = str(req) + '.json'
		print "Ficheiro json carregado:", filename
		json = load(filename)
		
		# Create json file only with tweets from cluster
		# c = []
		for key, value in dic.iteritems():
			data = [json[i-1] for i in value]
			print str(key) + ': ' + str(len(data))
			write_file(data, key)
			# c.append(key)

		# Get data
		json_path = './static/temp/'
		jfile = get_clusters(json_path)
		c = [name.split('/')[3].split('.')[0] for name in jfile ]

		# return "Boa"		
		return render_template('app.html', clusters =  c, files = jfile)

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')