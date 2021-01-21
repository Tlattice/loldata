from markers.counters import *
from markers.frame import *
from markers.players import *
from markers.areas import *
from markers.names import *
from dynamic_model.rift import *
import os
import json
import configparser
from tqdm import tqdm
import numpy as np
import pymongo
import pickle
from scipy.sparse import csr_matrix, vstack
import bz2


TOWERS = {
#blue
#top
frozenset([1171, 3571]): [0, 3],#inhibitor
frozenset([1169, 4287]): [0, 2],#base
frozenset([1512, 6699]): [0, 1],#inner
frozenset([981, 10441]): [0, 0],#outer
frozenset([3203, 3208]): [1, 3],
frozenset([3651, 3696]): [1, 2],
frozenset([5048, 4812]): [1, 1],
frozenset([5846, 6396]): [1, 0],
frozenset([3452, 1236]): [2, 3],
frozenset([4281, 1253]): [2, 2],
frozenset([6919, 1483]): [2, 1],
frozenset([10504, 1029]): [2, 0],
frozenset([1748, 2270]): [3, 0],
frozenset([2177, 1807]): [3, 1],
frozenset([11261, 13676]): [4, 3],
frozenset([10481, 13650]): [4, 2],
frozenset([7943, 13411]): [4, 1],
frozenset([4318, 13875]): [4, 0],
frozenset([11598, 11667]): [5, 3],
frozenset([11134, 11207]): [5, 2],
frozenset([9767, 10113]): [5, 1],
frozenset([8955, 8510]): [5, 0],
frozenset([13604, 11316]): [6, 3],
frozenset([13624, 10572]): [6, 2],
frozenset([13327, 8226]): [6, 1],
frozenset([13866, 4505]): [6, 0],
frozenset([13052, 12612]): [7, 1],
frozenset([12611, 13084]): [7, 0]
}

class StatsTable:
    def __init__(self):
        self.table = np.zeros((10, 4))
    def __call__(self, statsframe):
        pid = statsframe['participantId']
        pid = ROLE[pid].value
        self.table[pid-1][0] = statsframe['totalGold']
        self.table[pid-1][1] = statsframe['xp']
        self.table[pid-1][2] = statsframe['minionsKilled']
        self.table[pid-1][3] = statsframe['jungleMinionsKilled']
    def clear(self):
        self.table = np.zeros((10, 4))
    def reindex(self, indexlist):
        self.table = self.table[indexlist]
    def v(self):
        return self.table.flatten()
        
class KillsTable:
    def __init__(self):
        # k, v, a
        # k: minions + red + blue
        self.table = np.zeros((11, 5, 6))
    def __call__(self, frame):
        kid = frame['killerId']
        vid = frame['victimId']
        vid = ROLE[vid].value
        if kid == 0:
            print("Minions executed player")
            self.table[0][(vid-1)%5][5] += 1
            return
        assp = frame['assistingParticipantIds'] + [kid]
        for a in assp:
            at = ROLE[a].value
            self.table[(kid-1)][(vid-1)%5][(at-1)%5] += 1
    def clear(self):
        self.table = np.zeros((11, 5, 6))
    def reindex(self, indexlist):
        self.table = self.table[indexlist]
    def v(self):
        return self.table.flatten()

class TowersTable:
    def __init__(self):
        # lane or area, champ, score
        self.table = np.zeros((8, 6))
    def __call__(self, frame):
        kid = frame['killerId']
        #kid = ROLE[kid].value
        assp = frame['assistingParticipantIds'] + [kid]
        pos = frozenset([frame['position']['x'], frame['position']['y']])
        index = TOWERS[pos]
        #print(ROLE)
        #print(assp)
        for a in assp:
            if(a == 0):
                #print("Minions destroyed tower")
                self.table[index[0]][5] += index[1]+1
                continue
            at = ROLE[a].value
            self.table[index[0]][(at)%5] += index[1]+1
    def clear(self):
        self.table = np.zeros((8, 6))
    def reindex(self, indexlist):
        self.table = self.table[indexlist]
    def v(self):
        return self.table.flatten()

class MonsterTable:
    def __init__(self):
        # DRAGON, BARON_NASHOR, RIFTHERALD
        self.table = np.zeros((11, 3))
    def __call__(self, frame):
        kid = frame['killerId']
        mt = frame['monsterType']
        if kid != 0:
            kid = ROLE[kid].value
        else:
            kid = 10
        if mt == 'DRAGON':
            mtid = 0
        elif mt == 'BARON_NASHOR':
            mtid = 1
        elif mt == 'RIFTHERALD':
            mtid = 2
        self.table[kid][mtid] = 1
    def clear(self):
        self.table = np.zeros((11, 3))
    def reindex(self, indexlist):
        self.table = self.table[indexlist]
    def v(self):
        return self.table.flatten()
        
dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
playsdb = dbclient["nplays"]
timescollection = playsdb["timelines"]
times = timescollection.find({})

st = StatsTable()
kt = KillsTable()
tt = TowersTable()
mt = MonsterTable()

results = []
for timeline in tqdm(times):
    # Game stats
    try:
        if(len(timeline[u'frames']) < 6):
            print("Team surrendered")
            continue
    except Exception as e:
        print("Error reading frames")
        print(e)
        continue
    try:
        ROLE = map_players_by_point({}, [frame[u'participantFrames'] for frame in timeline[u'frames'][1:8]])
        PID = get_PID(ROLE)
        #pslice = np.array([])
        pslice = []
        for raw_frames in timeline[u'frames']:
            for frame in Frames(raw_frames):
                if frame.type == TYPE.PLAYER_STAT:
                    st(frame.payload)
                elif frame.type == TYPE.CHAMPION_KILL:
                    kt(frame.payload)
                elif frame.type == TYPE.BUILDING_KILL:
                    #print(timeline['matchId'])
                    #print(frame.payload.timestamp)
                    tt(frame.payload)
                elif frame.type == TYPE.ELITE_MONSTER_KILL:
                    mt(frame.payload)
            # Save plays
            #pslice = np.concatenate((pslice, st.v(), kt.v(), tt.v(), mt.v() ))
            pslice.append( csr_matrix(list(np.concatenate((st.v(), kt.v(), tt.v(), mt.v() )) ) ))
            #print('slice ', len(pslice))
            # Save packages
            st.clear()
            kt.clear()
            tt.clear()
            mt.clear()
    except Exception as e:
        print("Passing...")
        print(e)
        continue
    #results.append(pslice.tolist())
    results.append(pslice)
    
print("Saving results...")
with open('output/results.pkl', 'wb') as f:
    pickle.dump( results, f )
