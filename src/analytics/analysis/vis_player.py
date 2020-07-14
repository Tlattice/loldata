from timeline.counters import *
from timeline.frame import *
from timeline.players import *
from timeline.areas import *
import pickle
import numpy as np
from sklearn.decomposition import PCA
from scipy.cluster.vq import vq, kmeans, whiten

with open('slices.pickle', 'rb') as handle:
    data = pickle.load(handle)

# Compute average and standart deviation
arr = []
for x in data:
    p = x[0]
    arr.append(x[1]['blue'])
    arr.append(x[1]['red'])
arr = np.array(arr)
#avg = np.average(arr, axis=0)
#std = np.std(arr, axis=0)
#print arr.shape
re = np.reshape(arr, (12624, 5*5*5))
#print arr[1]
#print re[1]
#pca = PCA(n_components=80)
#pca.fit(re)
#print(sum(pca.explained_variance_ratio_))

whitened = whiten(re)
print kmeans(whitened, 5*5)

"""
l = []
for x in data:
    p = x[0]
    if TEAM.B_JG in p:
        if p[TEAM.B_JG] == 141:
            l.append(x[1]['blue'])
    if TEAM.R_JG in p:
        if p[TEAM.R_JG] == 141:
            l.append(x[1]['red'])

s = np.array(l)
champ_avg = np.average(s, axis=0)
champ_std = np.std(s, axis=0)

print (l[12]-avg)/std
"""

"""
print len(l)
print s
rd = ['top', 'mid', 'adc', 'supp', 'jg']
for i in range(len(s)):
    for j in range(len(s[0])):
        for k in range(len(s[0][0])):
            if s[i][j][k] > 1:
                print "------------------"
                print s[i][j][k]
                print "for"
                print '['+rd[i]+']['+rd[j]+']['+rd[k]+']'

"""
