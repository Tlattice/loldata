from timeline.counters import *
from timeline.frame import *
from timeline.players import *
from timeline.areas import *
import numpy as np
import os
import json
#import pickle
import cPickle

MP = '/home/user/Documents/git/loldata/src/match/'
TP = '/home/user/Documents/git/loldata/src/time/'

def normalize_matrix(matrix, number=False):
    if np.sum(matrix) == 0:
        print "No kills(?)"
        return False
    if not number:
        s = np.sum(matrix['red']) + np.sum(matrix['blue'])
    else:
        s = number
    #s = np.sum(matrix['red'])
    if not s == 0:
            matrix['red'] = matrix['red']/s
    #s = np.sum(matrix['blue'])
    if not s == 0:
            matrix['blue'] = matrix['blue']/s
    return s

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
            return lambda x: x[0] == TYPE.CHAMPION_KILL and x[1][u'victimId'] == PID[TEAM(z)] and PID[TEAM(i)] == x[1][u'killerId']# and len(x[1][u'assistingParticipantIds'])==0
        else:
            return lambda x: x[0] == TYPE.CHAMPION_KILL and x[1][u'victimId'] == PID[TEAM(z)] and PID[TEAM(j)] in x[1][u'assistingParticipantIds'] and PID[TEAM(i)] == x[1][u'killerId']
    for i in range(a[0], a[1]):
        for j in range(a[0], a[1]):
            for z in range(b[0], b[1]):
                ind = Marker(
                        str(i)+str(j)+str(z),
                        Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: False),
                        Counter(gencond(i, j, z), lambda x: False)
                        )
                indicators.append(ind)
    return indicators

filenames = []
for filename in os.listdir(MP):
    filenames.append(filename[:-5])
match = []
framed = []
res = []
counter = 0
out = []
f = open('wonAndClass.pkl', 'wb')
pickler = cPickle.Pickler(f)
for filename in filenames:
    try:
        with open(MP+filename+'.json') as file:
            match = json.loads(file.read())
        with open(TP+'{}_timeline.json'.format(filename)) as file:
            framed = json.loads(file.read())
    except:
        print "There was an error opening those files."
        continue
    TS = ['red', 'blue']
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
        print "File not valid (?)"
        continue
    try:
        ROLE = map_players_by_point(ps, pfs)
    except:
        print "An error mapping players (maybe an afk?)"
        continue
    PID = get_PID(ROLE)
    for k in TS:
        indicators = create_markers(k)
        # Execute markers for every frame in the timeline json
        try:
            for t in framed[u'frames']:
                for f in Frame(t):
                    for ind in indicators:
                        ind(f)
        except Exception as e:
            print "Error executing indicators: ", e
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
            
    gd = float(match[u'gameDuration'])/60
    bluewon = match[u'teams'][0][u'win']
    sm = normalize_matrix(matrix, gd)
    res = {}
    for participant in match[u'participants']:
        pid = participant[u'participantId']
        team = 'blue' if pid<6 else 'red'
        res[pid] = []
        stats = participant[u'stats']
        
        # Not bounded
        res[pid].append(stats[u'magicDamageDealt']/gd)
        res[pid].append(stats[u'physicalDamageDealt']/gd)
        res[pid].append(stats[u'trueDamageDealt']/gd)
        res[pid].append(stats[u'magicDamageDealtToChampions']/gd)
        res[pid].append(stats[u'physicalDamageDealtToChampions']/gd)
        res[pid].append(stats[u'trueDamageDealtToChampions']/gd)
        res[pid].append(stats[u'totalHeal']/gd)
        res[pid].append(stats[u'damageSelfMitigated']/gd)
        res[pid].append(stats[u'damageDealtToObjectives']/gd)
        res[pid].append(stats[u'damageDealtToTurrets']/gd)
        res[pid].append(stats[u'visionScore']/gd)
        res[pid].append(stats[u'timeCCingOthers']/gd)
        res[pid].append(stats[u'magicalDamageTaken']/gd)
        res[pid].append(stats[u'physicalDamageTaken']/gd)
        res[pid].append(stats[u'trueDamageTaken']/gd)
        res[pid].append(stats[u'goldEarned']/gd)
        res[pid].append(stats[u'totalMinionsKilled']/gd)
        res[pid].append(stats[u'neutralMinionsKilled']/gd)
        res[pid].append(stats[u'neutralMinionsKilledTeamJungle']/gd)
        res[pid].append(stats[u'neutralMinionsKilledEnemyJungle']/gd)
        res[pid].append(stats[u'totalTimeCrowdControlDealt']/gd)
        res[pid].append(stats[u'visionWardsBoughtInGame']/gd)
        res[pid].append(stats[u'sightWardsBoughtInGame']/gd)
        res[pid].append(stats[u'wardsPlaced']/gd)
        res[pid].append(stats[u'wardsKilled']/gd)
        
        # Might increase with time, but it's bounded
        res[pid].append(stats[u'champLevel'])
        res[pid].append(stats[u'inhibitorKills'])
        res[pid].append(stats[u'longestTimeSpentLiving'])
        res[pid].append(stats[u'turretKills'])
        res[pid].append(stats[u'totalUnitsHealed'])
        res[pid].append(stats[u'turretKills'])
        res[pid].append(stats[u'largestCriticalStrike'])
        
        # Time playing
        res[pid].append(gd)
        ast = np.reshape(matrix[team][:, pid%5, :], (25))
        ks = np.reshape(matrix[team][:, :, pid%5], (25))
        vs = np.reshape(matrix['red' if team == 'blue' else 'blue'][pid%5, :, :], (25))
        res[pid] = res[pid] + list(np.concatenate((ast, ks, vs)))
    
    print "Pickling!!!"
    rolmap = [0]*10
    for x in res:
        #print ROLE[x-1].value
        rolmap[ROLE[x-1].value] = res[x]
    pickler.dump([rolmap, bluewon ])
    print [rolmap, bluewon ]
    print "-----------------------------------------------"
    #break
    counter += 1
    print counter

f.close()
#with open('class.pickle', 'wb') as handle:
    #pickle.dump(out, handle, protocol=pickle.HIGHEST_PROTOCOL)
