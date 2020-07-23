from timeline.counters import *
from timeline.frame import *
from timeline.players import *
from timeline.areas import *
import numpy as np
import os
import json
import pickle

filenames = []
for filename in os.listdir(os.getcwd()+'/timeline/mount/'):
    filenames.append(filename[:-5])
match = []
framed = []
res = []
counter = 0

points = {
'top':[],
'mid':[],
'adc':[],
'supp':[],
'jg':[]
}

for filename in filenames:
    # Open match and timeline
    try:
        with open('timeline/mount/'+filename+'.json') as file:
            match = json.loads(file.read())
        with open('timeline/time/'+filename+'_timeline.json') as file:
            framed = json.loads(file.read())
    except:
        print "There was an error opening the file."
        continue
    # Participants frames
    try:
        ps = match[u'participants']
    except:
        print "Error: Data not found?"
        continue
    try:
        pfs = [x[u'participantFrames'] for x in framed[u'frames']][1:5]
    except:
        print "file not valid (?)"
        continue
    # Map roles
    try:
        ROLE = map_players_by_point(ps, pfs)
    except:
        print "An error mapping players (maybe an afk?)"
        continue
    PID = get_PID(ROLE)
    try:
        for t in framed[u'frames']:
            for f in Frame(t):
                    if f[0] == TYPE.PLAYER_STAT:
                        print ROLE
                        pos = [f[1][u'position'][u'x'], f[1][u'position'][u'y']]
                        if ROLE[f[1][u'participantId']-1] == TEAM.R_TOP or ROLE[f[1][u'participantId']-1] == TEAM.B_TOP:
                            points['top'].append(pos)
                        elif ROLE[f[1][u'participantId']-1] == TEAM.R_MID or ROLE[f[1][u'participantId']-1] == TEAM.B_MID:
                            points['mid'].append(pos)
                        elif ROLE[f[1][u'participantId']-1] == TEAM.R_ADC or ROLE[f[1][u'participantId']-1] == TEAM.B_ADC:
                            points['adc'].append(pos)
                        elif ROLE[f[1][u'participantId']-1] == TEAM.R_SUPP or ROLE[f[1][u'participantId']-1] == TEAM.B_SUPP:
                            points['supp'].append(pos)
                        elif ROLE[f[1][u'participantId']-1] == TEAM.R_JG or ROLE[f[1][u'participantId']-1] == TEAM.B_JG:
                            points['jg'].append(pos)
                            
    except Exception as e:
        print "Error:", e
        continue

    print counter
    counter += 1
with open('points.pickle', 'wb') as handle:
    pickle.dump(points, handle, protocol=pickle.HIGHEST_PROTOCOL)
