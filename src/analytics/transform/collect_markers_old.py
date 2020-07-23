from markers.counters import *
from markers.frame import *
from markers.players import *
from markers.areas import *
from scipy.spatial.distance import cdist
import json
import pickle


MATCH_PATH = 'output/match/'
TIMELINE_PATH = 'output/time/'

ACCID = 'y1FedHEKJzG1PQfnStt0OOIfQ4j9VydMpT5tfKUjjn9UAz_USVIYXgFm'
with open('players.pickle', 'rb') as handle:
    data = pickle.load(handle)
games = data[ACCID]
champs = [f[1] for f in games]
filenames = [str(f[0]) for f in games]
print "filename = ", filenames[0]

data = []
match = []
framed = []
ids = []
for filename in filenames:
    with open(filename+'.json') as file:
        match.append(json.loads(file.read()))
        temp = [x[u'participantId'] for x in match[-1][u'participantIdentities'] if x[u'player'][u'accountId']==ACCID]
        team = 'blue' if temp[0]<6 else 'red'
        ids.append(team)
    with open('../time/'+filename+'_timeline.json') as file:
        framed.append(json.loads(file.read()))

#-----------------------------------------------------------------------
#                               Markers
#-----------------------------------------------------------------------
#indicators = []
def create_marker():
    indicators = []
    #-----------------------------------------------------------------------
    #                               Jungle
    #-----------------------------------------------------------------------
    # How many times the jungle came and help some line before destroying a
    # tower.
    harassment_blue = Marker(
    "Number of times that red jungle was found in blue jungle",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.PLAYER_STAT and \
            ROLE[x[1][u'participantId']]==TEAM.R_JG and \
            INBLUEJG( (x[1][u'position'][u'x'], x[1][u'position'][u'y']) ),
            lambda x: False)
    )
    
    harassment_red = Marker(
    "Number of times that blue jungle was found in red jungle",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.PLAYER_STAT and \
            ROLE[x[1][u'participantId']]==TEAM.B_JG and \
            INREDJG( (x[1][u'position'][u'x'], x[1][u'position'][u'y']) ),
            lambda x: False)
    )
    
    """
    dragin_times = Marker(
    "Enemy jg kills by red",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            x[1][u'victimId'] == PID[TEAM.B_JG] and\
            (PID[TEAM.R_JG] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.R_JG] == x[1][u'killerId']), lambda x: False)
    )
    """
    indicators += harassment_blue, harassment_red
    # 
    #-----------------------------------------------------------------------
    #                               Middle
    #-----------------------------------------------------------------------
    
    #indicators += ganks_of_mid_top_r, ganks_of_mid_bot_r, ganks_of_mid_top_b
    
    #-----------------------------------------------------------------------
    #                               Top
    #-----------------------------------------------------------------------
    
    #indicators += ganks_of_top_mid_r, ganks_of_top_bot_r, ganks_of_mid_top_b
    
    #-----------------------------------------------------------------------
    #                               ADC
    #-----------------------------------------------------------------------
    
    #indicators += ganks_of_adc_top_r, ganks_of_adc_mid_b, ganks_of_adc_top_b
    
    #-----------------------------------------------------------------------
    #                               Support
    #-----------------------------------------------------------------------
    
    #indicators += ganks_of_supp_top_r, ganks_of_supp_mid_b, ganks_of_supp_top_b
    
    #-----------------------------------------------------------------------
    #                               Misc
    #-----------------------------------------------------------------------
    
    # Numbers of tower destroyed alone (split push)
    # Number of times that died near enemies or enemy area
    # Number of times that killed near enemies or enemy area
    # Measure group cohesion and snowballing(tendency to be grouped or alone) at late
    # Measure lane domain percentage(30% - 70%) and push power
    # How many times died or killed under a allied or enemy turret
    # Effect of some piece of equipment on lane domain percentage
    # Response time
    # Number of times that died at some point
    
    class peel_stack:
        def __init__(self):
            self.empty_stack()
            self.peel_res = []
            self.counter = 0
            self.mapping = {
                TEAM.R_TOP:0,
                TEAM.R_MID:1,
                TEAM.R_ADC:2,
                TEAM.R_SUPP:3,
                TEAM.R_JG:4,
                TEAM.B_TOP:5,
                TEAM.B_MID:6,
                TEAM.B_ADC:7,
                TEAM.B_SUPP:8,
                TEAM.B_JG:9,
            }
        def __call__(self, pos, role=False):
            self.peel_stack[self.mapping[role]] = [pos[u'x'], pos[u'y']]
            return False
        def peel_pop(self, val):
            if val:
                res = cdist(self.peel_stack, self.peel_stack)
                self.empty_stack()
                self.peel_res.append(res)
            return val
        def empty_stack(self):
            self.peel_stack = [[0, 0] for i in range(10)]
    
    ps = peel_stack()
    peeling = Marker(
    "positions",
    Trigger(lambda f: f[0] == TYPE.PLAYER_STAT,
            lambda f: ps.peel_pop( f[0] != TYPE.PLAYER_STAT) ),
    Counter( lambda x: ps(x[1][u'position'], ROLE[x[1][u'participantId']]),
             lambda x: False)
    )
    
    indicators += [peeling]
    return indicators
#-----------------------------------------------------------------------
#                               Main
#-----------------------------------------------------------------------
for i in range(len(framed)):
    print "Processing game"
    print "team:"
    print ids[i]
    print champs[i]
    #print "Processing frames"
    map_players(match[i][u'participants'])
    PID = get_PID()
    indicators = create_marker()
    try:
        for t in framed[i][u'frames']:
            for f in Frame(t):
                for ind in indicators:
                    ind(f)
    except Exception as e:
        print "Error---------------------------------------------------"
        print e
        print PID
        print "Error---------------------------------------------------"
        continue
    for ind in indicators:
        ind.printl()
    print "------------------------------------------------------------"
    #break
    
