from flask import Flask, request, render_template, url_for
from numpy import *
import os

app = Flask(__name__)

def get_clusters(path):
    """    Returns a list of folders for 
        all clusters images in a directory. """ 
    return [os.path.join(path,f) for f in os.listdir(path) if not f.endswith('.DS_Store')]

def get_urls(path):
    """    Returns a list of filenames for 
        all jpg images in a directory. """ 
    return [os.path.join(path,f) for f in os.listdir(path)]

@app.route('/')
def start():
	return render_template('index.html')

@app.route('/cluster', methods= ['GET', 'POST'])
def cluster():
	req = request.form['subset']

	path = 'static/img/' + str(req)
	folders = get_clusters(path)
	print folders
	clusters = []
	for cluster in folders:
		clusters.append(get_urls(cluster))
	return render_template('app.html', clusters = clusters, req = req)

if __name__ == '__main__':
	# app.debug = True
	app.run(host='0.0.0.0')