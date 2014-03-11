import sift

import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

imname = 'empire.jpg'
im1 = np.array(Image.open(imname).convert('L')) 
sift.process_image(imname,'empire.sift')
l1,d1 = sift.read_features_from_file('empire.sift')
plt.figure()
plt.gray()
sift.plot_features(im1,l1,circle=True)
plt.show()
