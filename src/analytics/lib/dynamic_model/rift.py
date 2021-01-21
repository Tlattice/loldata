from markers.areas import *
from markers.frame import *
import numpy as np

TOWER_RANGE = 750
TOWER, INHIBITOR = 1, 0

# TODO: Put these routines in other lib
def distance(posa, posb):
    if type(posa) is dict:
        rposa = np.array([posa[u'x'], posa[u'y']])
    else:
        rposa = np.array(posa)
    if type(posb) is dict:
        rposb = np.array([posb[u'x'], posb[u'y']])
    else:
        rposb = np.array(posb)
    return np.linalg.norm(rposa-rposb)
    
def vector(pos):
    res = np.array([pos[u'x'], pos[u'y']])
    return res

def project_onto(x, y):
    return np.dot(x, y) / np.linalg.norm(y)

class minute:
    def __init__(self, number, ep = 0.001):
        self.number = number*60000
        self.ep = ep
    def __eq__(self, other):
        #print(self.number*(1-self.ep))
        #print(self.number*(1+self.ep))
        return (self.number*(1-self.ep) < other) and (other < self.number*(1+self.ep))
    def __gt__(self, other): 
        if(self.number>other*(1-self.ep)): 
            return True
        else: 
            return False
    def __ge__(self, other): 
        if(self.number>=other*(1-self.ep)): 
            return True
        else: 
            return False
    def __lt__(self, other): 
        if(self.number<other*(1+self.ep)): 
            return True
        else: 
            return False
    def __le__(self, other): 
        if(self.number<=other*(1+self.ep)): 
            return True
        else: 
            return False

class Building:
    def __init__(self, pos, btype):
        self._pos = np.array(pos)
        self.position = {u'x':pos[0], u'y':pos[1]}
        self.pos = pos # Accessible attribute
        self.standing = True
        self.btype = btype
    def destroy(self):
        self.standing = False
    def regenerate(self):
        self.standing = True
    def inrange(self, ppos):
        if self.standing and self.btype == TOWER:
            dist = np.linalg.norm(self._pos-ppos)
            if dist <= TOWER_RANGE:
                return True
            else:
                return False
        else:
            return False

class DictX(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return '<DictX ' + dict.__repr__(self) + '>'

class Rift(dict):
    def __init__(self):
        # Structure
        super(Rift, self).__init__({
            'blue':DictX({
            # outer - inner
            # 3T - 2T - 1T - 0I
            'top':DictX({'inhibitor': Building([1171, 3571], INHIBITOR),
                   'base': Building([1169, 4287], TOWER),
                   'inner': Building([1512, 6699], TOWER),
                   'outer': Building([981, 10441], TOWER)}),
            'mid':DictX({'inhibitor': Building([3203, 3208], INHIBITOR),
                   'base': Building([3651, 3696], TOWER),
                   'inner': Building([5048, 4812], TOWER),
                   'outer': Building([5846, 6396], TOWER)}),
            'bot':DictX({'inhibitor': Building([3452, 1236], INHIBITOR),
                          'base': Building([4281, 1253], TOWER),
                          'inner': Building([6919, 1483], TOWER),
                          'outer': Building([10504, 1029], TOWER)}),
            'base':DictX({
                'left': Building([1748, 2270], TOWER),
                'right': Building([2177, 1807], TOWER)
            })
            }),
            'red':DictX({
            'top':DictX({'inhibitor': Building([11261, 13676], INHIBITOR),
                         'base': Building([10481, 13650], TOWER),
                         'inner': Building([7943, 13411], TOWER),
                         'outer': Building([4318, 13875], TOWER)}),
            'mid':DictX({'inhibitor': Building([11598, 11667], INHIBITOR),
                        'base': Building([11134, 11207], TOWER),
                        'inner': Building([9767, 10113], TOWER),
                        'outer': Building([8955, 8510], TOWER)}),
            'bot':DictX({'inhibitor': Building([13604, 11316], INHIBITOR),
                         'base': Building([13624, 10572], TOWER),
                         'inner': Building([13327, 8226], TOWER),
                         'outer': Building([13866, 4505], TOWER)}),
            'base':DictX({
                'left':Building([13052, 12612], TOWER),
                'right':Building([12611, 13084], TOWER),
            })
        })
        })
    def __call__(self, frame):
        if frame.type == TYPE.BUILDING_KILL:
            lane = frame.payload.laneType
            towertype = frame.payload.towerType
            team = 'blue' if frame.payload.teamId==100 else 'red'
            if 'NEXUS' in towertype:
                if [frame.payload.position.x, frame.payload.position.y] == self[team].base.left.pos:
                    self[team].base.left.destroy()
                else:
                    self[team].base.right.destroy()
            else:
                if 'OUTER' in towertype:
                    towerpos = 'outer'
                elif 'INNER' in towertype:
                    towerpos = 'inner'
                elif 'BASE' in towertype:
                    towerpos = 'base'
                elif 'UNDEFINED' in towertype:
                    towerpos = 'inhibitor'
                if 'TOP' in lane:
                    self[team].top[towerpos].destroy()
                elif 'MID' in lane:
                    self[team].mid[towerpos].destroy()
                elif 'BOT' in lane:
                    self[team].bot[towerpos].destroy()
        elif frame.type == TYPE.ELITE_MONSTER_KILL:
            pass
        elif frame.type == TYPE.PLAYER_STAT:
            # update time
            pass
    def clean(self):
        for team in self.values():
            for lane in team.values():
                for tower in lane.values():
                    tower.regenerate()
    # Dictionary methods
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)
