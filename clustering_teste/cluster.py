import scipy
import pyparsing
import matplotlib.pyplot as mat
import numpy as np
from scipy.cluster.vq import *


class1 = 1.5 * np.random.randn(100,2)
class2 = np.random.randn(100,2) + np.array([5,5])
features = np.vstack((class1,class2))

centroids,variance = kmeans(features,2)

code,distance = vq(features,centroids)

# figure()
ndx = np.where(code==0)[0] 
mat.plot(features[ndx,0],features[ndx,1],'*') 
ndx = np.where(code==1)[0] 
mat.plot(features[ndx,0],features[ndx,1],'r.') 
mat.plot(centroids[:,0],centroids[:,1],'go') 
mat.axis('off')
mat.show()