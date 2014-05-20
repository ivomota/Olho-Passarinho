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
	path = 'static/img/'
	folders = get_clusters(path)
	print folders
	clusters = []
	for cluster in folders:
		clusters.append(get_urls(cluster))
	return render_template('index.html', clusters = clusters)

# @app.route('/cluster', methods=['GET', 'POST'])
# def cluster():
# 	path = 'static/img/'
# 	folders = get_clusters(path)
# 	print folders
# 	clusters = []
# 	for cluster in folders:
# 		clusters.append(get_urls(cluster))
# 	return render_template('app.html', clusters = clusters)

if __name__ == '__main__':
	app.debug = True
	app.run()