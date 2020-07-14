from timeline.counters import *
from timeline.frame import *
from timeline.players import *
from timeline.areas import *
import numpy as np
import os
import json
import pickle

def normalize_matrix(matrix):
    if np.sum(matrix) == 0:
        print "No kills(?)"
        return False
    #s = np.sum(matrix['red']) + np.sum(matrix['blue'])
    s = np.sum(matrix['red'])
    if not s == 0:
            matrix['red'] = matrix['red']/s
    s = np.sum(matrix['blue'])
    if not s == 0:
            matrix['blue'] = matrix['blue']/s

def create_markers(team = 'red'):
    if team == 'red':
        a = [5, 10]
        b = [0, 5]
    else:
        a = [0, 5]
        b = [5, 10]
        
    indicators = []
    def gencond(i, j, z):
        if i == j:
            return lambda x: x[0] == TYPE.CHAMPION_KILL and x[1][u'victimId'] == PID[TEAM(z)] and PID[TEAM(i)] == x[1][u'killerId'] and len(x[1][u'assistingParticipantIds'])==0
        else:
            return lambda x: x[0] == TYPE.CHAMPION_KILL and x[1][u'victimId'] == PID[TEAM(z)] and PID[TEAM(j)] in x[1][u'assistingParticipantIds'] and PID[TEAM(i)] == x[1][u'killerId']
    for i in range(a[0], a[1]):
        for j in range(a[0], a[1]):
            for z in range(b[0], b[1]):
                ind = Marker(
                        str(i)+str(j)+str(z),
                        Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
                        Counter(gencond(i, j, z), lambda x: False)
                        )
                indicators.append(ind)
    return indicators

filenames = []
for filename in os.listdir(os.getcwd()):
    filenames.append(filename[:-5])
match = []
framed = []
res = []
counter = 0
for filename in filenames:
    try:
        with open(filename+'.json') as file:
            match = json.loads(file.read())
        with open('../time/'+filename+'_timeline.json') as file:
            framed = json.loads(file.read())
    except:
        print "There was an error."
        continue
    ts = ['red', 'blue']
    matrix = {'red': np.array([[[0]*5]*5]*5, dtype=float),
              'blue': np.array([[[0]*5]*5]*5, dtype=float)}
    try:
        map_players(match[u'participants'])
        ps = match[u'participants']
    except:
        print "Error: Data not found?"
        continue
    try:
        pfs = [x[u'participantFrames'] for x in framed[u'frames']][1:5]
    except:
        print "file not valid (?)"
        continue
    try:
        ROLE = map_players_by_point(ps, pfs)
    except:
        print "An error mapping players(maybe an afk?)"
        continue
    PID = get_PID(ROLE)
    for k in ts:
        indicators = create_markers(k)
        try:
            for t in framed[u'frames']:
                for f in Frame(t):
                    for ind in indicators:
                        ind(f)
        except Exception as e:
            print "Error:", e
            continue
        for ind in indicators:
            g, j, z = int(ind.desc()[0]), int(ind.desc()[1]), int(ind.desc()[2])
            if k == 'red':
                pij = 5
                pz = 0
            else:
                pij = 0
                pz = 5
            matrix[k][z-pz][g-pij][j-pij] = ind.count()
    normalize_matrix(matrix)
    cdict = champ_id_match(ps, ROLE)
    res.append([cdict, matrix])
    print counter
    counter += 1

with open('slices.pickle', 'wb') as handle:
    pickle.dump(res, handle, protocol=pickle.HIGHEST_PROTOCOL)
