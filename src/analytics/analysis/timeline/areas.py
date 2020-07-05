from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from scipy.spatial.distance import cdist

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
BLUE_JG_RED_POLYGON = Polygon(BLUE_JG_RED)
BLUE_JG_BLUE_POLYGON = Polygon(BLUE_JG_BLUE)
RED_JG_RED_POLYGON = Polygon(RED_JG_RED)
RED_JG_BLUE_POLYGON = Polygon(RED_JG_BLUE)

def INBLUEJG(point):
    p = Point(point[0], point[1])
    return BLUE_JG_RED_POLYGON.contains(p) or BLUE_JG_BLUE_POLYGON.contains(p)

def INREDJG(point):
    p = Point(point[0], point[1])
    return RED_JG_RED_POLYGON.contains(p) or RED_JG_BLUE_POLYGON.contains(p)

def distance(pos1, pos2):
    a = [[pos1[u'x'], pos1[u'y']]]
    b = [[pos2[u'x'], pos2[u'y']]]
    return scipy.cdist(a,b)

