import json
import os
import pickle
from itertools import combinations as comb
from itertools import permutations as per

path = '../../match/'
players = {}
for filename in os.listdir(path):
    with open(os.path.join(path, filename), 'r') as f:
        try:
            data = json.loads(f.read())
        except ValueError:
            print "There was an error opening a file"
            continue
        if not u'participants' in data:
            print "No participants listed :s"
            continue
        if not u'gameId' in data:
            print "No gameId listed :s"
            continue
        gid = data[u'gameId']
        #p = [x[u'player'][u'accountId'] for x in data[u'participantIdentities']]
        p = {}
        for i in range(len(data[u'participantIdentities'])):
            accid = data[u'participantIdentities'][i][u'player'][u'accountId']
            role = data[u'participants'][i][u'timeline'][u'role']
            lane = data[u'participants'][i][u'timeline'][u'lane']
            champ = data[u'participants'][i][u'championId']
            p[accid] = [role+'_'+lane, champ]
        print p
        for x in p:
            if x in players:
                print "player found"
                players[x].append([gid, p[x]])
            else:
                print "new player"
                players[x] = [[gid, p[x]]]

with open('players.pickle', 'wb') as handle:
    pickle.dump(players, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
