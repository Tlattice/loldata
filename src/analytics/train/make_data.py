import numpy as np
from collections import OrderedDict
from GHSOM import GHSOM
import json
import pickle

def neval(ghsom, data):
    distances = list()
    _neuron = ghsom
    nid = []
    count = 0
    while _neuron.child_map is not None:
        #print("Diving...")
        nid.append(4*_neuron.position[0]+_neuron.position[1])
        _gsom = _neuron.child_map
        _neuron = _gsom.winner_neuron(data)[0][0]
        count += 1
    while count<5:
        nid.append(0)
        count += 1
    return(_neuron, nid)

if __name__ == '__main__':
    print("Loading model...")
    with open('output/classify_model.model', 'rb') as fp:
        model = pickle.load(fp)
    print("Done")
    print("Loading data...")
    with open('output/results.json', 'r') as f:
        data = json.load(f)
    print("Done")
    
    #input_data = np.array( data.values(), dtype=float)
    training_data = {'vectors':[], 'labels':[]}
    for k in data:
        if not '_bluewon' in k:
            training_data['labels'].append(data[k+'_bluewon'])
            team = data[k]
            batch = []
            for player in team:
                nplayer = np.array(player, dtype=float)
                neuron, nid = neval(model, nplayer)
                batch.append(nid)
            training_data['vectors'].append(np.array(batch, dtype=float))
    print("Saving training data...")
    with open('output/training_data.pkl', 'wb') as f:
        pickle.dump(training_data, f)
