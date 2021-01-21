import numpy as np
from collections import OrderedDict
from GHSOM import GHSOM
import json
import pickle

if __name__ == '__main__':
    print("Loading model...")
    with open('output/classify_model.model', 'rb') as fp:
        model = pickle.load(fp)
    print("Done")
    print("Loading data...")
    with open('output/results.json', 'r') as f:
        data = json.load(f)
    print("Done")
    print(model)
