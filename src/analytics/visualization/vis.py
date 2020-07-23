
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import numpy as np

import pickle

with open('teams3.pickle', 'rb') as handle:
    data = pickle.load(handle)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for k in data.keys():
    v = data[k]
    #print v
    if True:
        ax.scatter(v[0], v[1], v[3])
        print k
        print v[0], v[1], v[2], v[3]

ax.set_xlabel('Kills Label')
ax.set_ylabel('Deaths Label')
ax.set_zlabel('Assists Label')

plt.show()

