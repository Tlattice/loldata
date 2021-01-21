from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from scipy.spatial.distance import cdist
from dynamic_model.rift import *

BLUE_JG_BLUE =  [(4140, 5200), 
            (4100, 5350), 
            (1950, 5950), 
            (1850, 10550), 
            (2800, 10850), 
            (4150, 9100), 
            (5800, 8450)]
            
BLUE_JG_RED =  [(5870, 1980), 
                (5250, 4300), 
                (6950, 6050), 
                (9450, 4750), 
                (9900, 3750), 
                (10950, 3900), 
                (11500, 2100)]
                
RED_JG_RED = [(4430, 13060), 
               (4800, 11400), 
               (5750, 10900), 
               (5950, 9700), 
               (8050, 9000), 
               (10000, 10850), 
               (9300, 13150)]
               
RED_JG_BLUE = [(9350, 6550), 
                (9800, 8650), 
                (10750, 9600), 
                (12900, 9050), 
                (13150, 4450)]
RED_TOP = [(1870, 14620), (700, 11600), (1000, 13900), (4000, 14400), (9600, 14400), (9600, 13300), (3300, 12800), (2800, 12200)]
BLUE_TOP = [(500, 5700), (1900, 5800), (1900, 11000), (2800, 12200), (3700, 13000), (3200, 14300), (2300, 13800)]
RED_MID = [(6400, 7600), (7400, 6400), (11400, 10500), (10500, 11200)]
BLUE_MID = [(3700, 4800), (4700, 3800), (8500, 7600), (7400, 8500)]
RED_BOT = [(13100, 9600), (14600, 9600), (14200, 400), (11700, 600), (11400, 2000), (13100, 3700)]
BLUE_BOT = [(4900, 2100), (4900, 500), (14300, 700), (14400, 3300), (1300, 3700), (11700, 2200)]


BLUE_JG_RED_POLYGON = Polygon(BLUE_JG_RED)
BLUE_JG_BLUE_POLYGON = Polygon(BLUE_JG_BLUE)
RED_JG_RED_POLYGON = Polygon(RED_JG_RED)
RED_JG_BLUE_POLYGON = Polygon(RED_JG_BLUE)

RED_TOP_POLYGON = Polygon(RED_TOP)
BLUE_TOP_POLYGON = Polygon(BLUE_TOP)
RED_MID_POLYGON = Polygon(RED_MID)
BLUE_MID_POLYGON = Polygon(BLUE_MID)
RED_BOT_POLYGON = Polygon(RED_BOT)
BLUE_BOT_POLYGON = Polygon(BLUE_BOT)

#Using areas

def INBLUEJG(point):
    p = Point(point[u'x'], point[u'y'])
    return BLUE_JG_RED_POLYGON.contains(p) or BLUE_JG_BLUE_POLYGON.contains(p)

def INREDJG(point):
    if type(point) == dict:
        p = Point(point[u'x'], point[u'y'])
    else:
        p = Point(point[0], point[1])
    return RED_JG_RED_POLYGON.contains(p) or RED_JG_BLUE_POLYGON.contains(p)

def INREDTOP(point):
    if type(point) == dict:
        p = Point(point[u'x'], point[u'y'])
    else:
        p = Point(point[0], point[1])
    return RED_TOP_POLYGON.contains(p)

def INBLUETOP(point):
    if type(point) == dict:
        p = Point(point[u'x'], point[u'y'])
    else:
        p = Point(point[0], point[1])
    return BLUE_TOP_POLYGON.contains(p)

def INREDMID(point):
    if type(point) == dict:
        p = Point(point[u'x'], point[u'y'])
    else:
        p = Point(point[0], point[1])
    return RED_MID_POLYGON.contains(p)

def INBLUEMID(point):
    if type(point) == dict:
        p = Point(point[u'x'], point[u'y'])
    else:
        p = Point(point[0], point[1])
    return BLUE_MID_POLYGON.contains(p)

def INREDBOT(point):
    if type(point) == dict:
        p = Point(point[u'x'], point[u'y'])
    else:
        p = Point(point[0], point[1])
    return RED_BOT_POLYGON.contains(p)

def INBLUEBOT(point):
    if type(point) == dict:
        p = Point(point[u'x'], point[u'y'])
    else:
        p = Point(point[0], point[1])
    return BLUE_BOT_POLYGON.contains(p)


#def distance(pos1, pos2):
#    a = [[pos1[u'x'], pos1[u'y']]]
#    b = [[pos2[u'x'], pos2[u'y']]]
#    return scipy.cdist(a,b)

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

class Area(dict):
    def __init__(self):
        super(Area, self).__init__({
            'blue':DictX({'top': INBLUETOP,
                          'mid': INBLUEMID,
                          'bot': INBLUEBOT,
                          'jg':INBLUEJG
            }),
            'red': DictX({'top': INREDTOP,
                          'mid': INREDMID,
                          'bot': INREDBOT,
                          'jg':INREDJG
            })
            })
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)
