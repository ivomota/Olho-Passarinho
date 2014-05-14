import pickle
import math
from numpy import *
import sys

from rpy2.robjects import r
from rpy2.robjects.numpy2ri import numpy2ri

from datetime import datetime
from dateutil import parser


def load(filename, verbose=False):
    # Open file
    if verbose : print("Loading %s" % filename)
    pkl_file = open(filename, 'rb')
    # Load from Pickle file.
    data = pickle.load(pkl_file)
    pkl_file.close()
    return data

data = load('../tweets_instagram_final.pkl')
leng = len(data)
t1 = str(data[0]['created_at'])
t2 = str(data[1000]['created_at'])
print t1
print t2
yourDate1 = parser.parse(t1)
yourDate2 = parser.parse(t2)

print abs((yourDate2 - yourDate1).total_seconds())

# d = datetime.strptime(t, '%a %b %d %H:%M:%S %z %Y')
# print d.strftime('%Y-%m-%d');