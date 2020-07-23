import json
import os
import pickle
from itertools import combinations as comb
from itertools import permutations as per

path = 'timeline/mount'
grank = {}
times = {}

counter = 0
for filename in os.listdir(os.getcwd()):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        try:
            data = json.loads(f.read())
        except ValueError:
            print "There was an error opening"
            continue
        if not u'participants' in data:
            continue
        if not u'gameId' in data:
            continue
        win = []
        lose = []
        for p in data[u'participants']:
            name = str(p[u'championId'])+'_'+p[u'timeline'][u'lane']+'_'+p[u'timeline'][u'role']
            kills = p[u'stats'][u'kills']
            deaths = p[u'stats'][u'deaths']
            assists = p[u'stats'][u'assists']
            l = [name, kills, deaths, assists]
            if p[u'stats'][u'win']:
                l.append(1)
                win.append(l)
            else:
                l.append(-1)
                lose.append(l)
        def scale(l, index, rev=False):
            if not rev:
                score = range(1, 6)
            else:
                score = range(-1, -6, -1)
            for i in range(len(l)):
                l[i][index] = score[i]
        # Get scores
        def rank(l):
            for i in range(1, 4):
                s = sorted(win, key=lambda x: x[i])
                scale(s, i)
            return s
        win = rank(win)
        lose = rank(lose)
        #print win
        # Make combinations
        def unique(l):
            temp = {}
            for x in l:
                champ = []
                k = 0
                d = 0
                a = 0
                w = 0
                for y in x:
                    champ.append(y[0])
                    k += y[1]
                    d += y[2]
                    a += y[3]
                    w += y[4]
                temp[frozenset(champ)] = [k, d, a, w]
            return temp
        wincomb = list(comb(win, 3))
        wincomb = unique(wincomb)
        losecomb = list(comb(lose, 3))
        losecomb = unique(losecomb)
        #add to the global rank
        def mix(a, b):
            res = []
            for i in range(len(a)):
                res.append(a[i]+b[i])
            return res
        
        def fuse(w):
            for w in wincomb:
                for p in list(per(w)):
                    t = frozenset(p)
                    if t in grank:
                        #print "found!!!!!!!!!!!"
                        grank[t] = mix(grank[t], wincomb[t])
                        times[t] += 1
                        break
                else:
                    #print "adding", w
                    grank[w] = wincomb[w]
                    times[w] = 0
        fuse(wincomb)
        #print grank
        #fuse(wincomb)
        fuse(losecomb)
        #print wincomb
        #print list(comb)
        #break

# Normalize data
copy = {}
for k in grank:
    print "------------------------------------------------------------"
    print k
    print times[k]
    print grank[k]
    for i in range(len(grank[k])):
        grank[k][i] = float(grank[k][i])/times[k]
    print grank[k]
    if times[k] > 5:
        copy[k] = grank[k]

with open('teams3.pickle', 'wb') as handle:
    pickle.dump(copy, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
