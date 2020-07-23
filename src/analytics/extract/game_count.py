import json
import os
import pickle
from itertools import combinations as comb
from itertools import permutations as per

path = '../../match/'
with open('players.pickle', 'rb') as f:
    players = pickle.load(f)

games = []
playerstofetch = []
count = 0
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
        #print "Game ", gid
        p = {}
        addgame = True
        for i in range(len(data[u'participantIdentities'])):
            accid = data[u'participantIdentities'][i][u'player'][u'accountId']
            #print "Player ", accid
            if accid in players:
                if len(players[accid]) < 3:
                    playerstofetch.append(accid)
                    addgame = False
                else:
                    continue
        if addgame:
            games.append(gid)
            print "--------------- Game added ---------------"
        else:
            count += 1
            print "Game pending: ", count

with open('games.pickle', 'wb') as handle:
    pickle.dump(games, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('playerstofetch.pickle', 'wb') as handle:
    pickle.dump(playerstofetch, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
