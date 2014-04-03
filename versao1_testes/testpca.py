#-*- coding:utf-8 -*-

import imtools
import pca
from PIL import Image
import numpy as np
from matplotlib import pylab as ply
if __name__ == '__main__':
    imlist= imtools.get_imlist("../img/thumbs/")
    im  =   np.array(Image.open(imlist[0]))
    m,n =   im.shape[0:2]
    imnbr = len(imlist)
    
    immatrix = np.array([np.array(Image.open(im)).flatten() for im in imlist],'f')
    V,S,immean = pca.pca(immatrix)
    
    ply.figure()
    ply.gray()
    ply.subplot(2,4,1)
    ply.imshow(immean.reshape(m,n))
    for i in range(7):
        ply.subplot(2,4,i+2)
        ply.imshow(V[i].reshape(m,n))
    ply.show()
    