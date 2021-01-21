from markers.counters import *
from markers.frame import *
from markers.players import *
from markers.areas import *
from markers.names import *
from dynamic_model.rift import *
import numpy as np
import pickle
import bz2
import pymongo
from scipy.sparse import csr_matrix, vstack

dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
traindb = dbclient["train_data"]
processed_data = traindb["processed_data"]

def leniter(array):
    for x in array:
        yield len(x)

def extend(array):
    maxlen = max(leniter(data))
    ar = np.array(array[0])
    z = np.zeros((maxlen-len(ar)))
    na = np.concatenate((ar, z))
    res = csr_matrix(na, dtype=np.double)
    for i in range(1, len(array)):
        ar = np.array(array[i])
        z = np.zeros((maxlen-len(ar)))
        na = np.concatenate((ar, z))
        res = vstack( [res, csr_matrix(na, dtype=np.double)] )
        #na = {'data': np.concatenate((ar, z)).tolist()}
        #if len(na) != maxlen:
        #    print(i, ':')
        #    print(len(na))
        #processed_data.insert_one(na)
        #res.append(na)
    return res
    #return np.array(res)

print("Loading data...")
data = np.array(pickle.load(open('output/results.pkl', 'rb')))
print(data.shape)
print("Extending data.")
res = extend(data)
#extend(data)
#print(res.shape)
print("Saving results...")
with bz2.BZ2File('output/results_extended.pkl', 'wb') as f: 
    pickle.dump( res, f, protocol=4)
#with open('output/results_extended.pkl', 'wb') as f:
#    pickle.dump( res, f, protocol=4)
