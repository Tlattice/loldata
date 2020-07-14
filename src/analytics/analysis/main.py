from timeline.counters import *
from timeline.frame import *
from timeline.players import *
from timeline.areas import *

from scipy.spatial.distance import cdist
import json
import pickle
# ----------------------------------------------------------------------

MATCH_CONST = 'data/match_info.json'
FRAME_CONST = 'data/frame_info.json'
ACCID = 'y1FedHEKJzG1PQfnStt0OOIfQ4j9VydMpT5tfKUjjn9UAz_USVIYXgFm'
with open('players.pickle', 'rb') as handle:
    data = pickle.load(handle)
games = data[ACCID]
champs = [f[1] for f in games]
filenames = [str(f[0]) for f in games]
print "filename = ", filenames[0]

"""
for p in data:
    if len(data[p])>5:
        filenames = data[p]
        break
"""

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
    sucessful_ganks_top_r = Marker(
    "Successful top ganks by red jg",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            x[1][u'victimId'] == PID[TEAM.B_TOP] and\
            (PID[TEAM.R_JG] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.R_JG] == x[1][u'killerId']), lambda x: False)
    )
    sucessful_ganks_top_b = Marker(
    "Successful top ganks by blue jg",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            x[1][u'victimId'] == PID[TEAM.R_TOP] and\
            (PID[TEAM.B_JG] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.B_JG] == x[1][u'killerId']), lambda x: False)
    )
    sucessful_ganks_mid_r = Marker(
    "Successful mid ganks by red jg",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            x[1][u'victimId'] == PID[TEAM.B_MID] and\
            (PID[TEAM.R_JG] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.R_JG] == x[1][u'killerId']), lambda x: False)
    )
    sucessful_ganks_mid_b = Marker(
    "Successful mid ganks by blue jg",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            x[1][u'victimId'] == PID[TEAM.R_MID] and\
            (PID[TEAM.B_JG] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.B_JG] == x[1][u'killerId']), lambda x: False)
    )
    
    sucessful_ganks_bot_r = Marker(
    "Successful bot ganks by blue jg",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            (x[1][u'victimId'] == PID[TEAM.B_ADC] or x[1][u'victimId'] == PID[TEAM.B_SUPP]) and\
            (PID[TEAM.R_JG] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.R_JG] == x[1][u'killerId']), lambda x: False)
    )
    
    sucessful_ganks_bot_b = Marker(
    "Successful bot ganks by blue jg",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            (x[1][u'victimId'] == PID[TEAM.R_ADC] or x[1][u'victimId'] == PID[TEAM.R_SUPP]) and\
            (PID[TEAM.B_JG] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.B_JG] == x[1][u'killerId']), lambda x: False)
    )
    
    jg_kills_b = Marker(
    "Enemy jg kills by blue",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            x[1][u'victimId'] == PID[TEAM.R_JG] and\
            (PID[TEAM.B_JG] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.B_JG] == x[1][u'killerId']), lambda x: False)
    )
    
    jg_kills_r = Marker(
    "Enemy jg kills by red",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            x[1][u'victimId'] == PID[TEAM.B_JG] and\
            (PID[TEAM.R_JG] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.R_JG] == x[1][u'killerId']), lambda x: False)
    )
    
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
    
    time = Marker(
    "Time that it took to finish early game.",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.PLAYER_STAT and \
            ROLE[x[1][u'participantId']]==TEAM.B_JG,
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
    indicators += sucessful_ganks_top_r, sucessful_ganks_top_b, sucessful_ganks_mid_r, sucessful_ganks_mid_b, harassment_blue, \
                  sucessful_ganks_bot_r, sucessful_ganks_bot_b, jg_kills_r, jg_kills_b, harassment_red, time
    # 
    #-----------------------------------------------------------------------
    #                               Middle
    #-----------------------------------------------------------------------
    ganks_of_mid_top_r = Marker(
    "Successful top ganks by red mid",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            x[1][u'victimId'] == PID[TEAM.B_TOP] and\
            (PID[TEAM.R_MID] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.R_MID] == x[1][u'killerId']), lambda x: False)
    )
    
    ganks_of_mid_bot_r = Marker(
    "Successful bot ganks by red mid",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            (x[1][u'victimId'] == PID[TEAM.B_ADC] or x[1][u'victimId'] == PID[TEAM.B_SUPP]) and\
            (PID[TEAM.R_MID] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.R_MID] == x[1][u'killerId']), lambda x: False)
    )
    
    ganks_of_mid_top_b = Marker(
    "Successful top ganks by blue mid",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            x[1][u'victimId'] == PID[TEAM.R_TOP] and \
            (PID[TEAM.B_MID] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.B_MID] == x[1][u'killerId']), lambda x: False)
    )
    
    ganks_of_mid_bot_b = Marker(
    "Successful bot ganks by blue mid",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            (x[1][u'victimId'] == PID[TEAM.R_ADC] or x[1][u'victimId'] == PID[TEAM.R_SUPP]) and\
            (PID[TEAM.B_MID] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.B_MID] == x[1][u'killerId']), lambda x: False)
    )
    
    front_kills_mid_r = Marker(
    "Early red mid enemy kills",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            (x[1][u'victimId'] == PID[TEAM.B_MID]) and\
            (PID[TEAM.R_MID] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.R_MID] == x[1][u'killerId']), lambda x: False)
    )
    
    front_kills_mid_b = Marker(
    "Early blue mid enemy kills",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            (x[1][u'victimId'] == PID[TEAM.R_MID]) and\
            (PID[TEAM.B_MID] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.B_MID] == x[1][u'killerId']), lambda x: False)
    )
    
    indicators += ganks_of_mid_top_r, ganks_of_mid_bot_r, ganks_of_mid_top_b,\
                  ganks_of_mid_bot_b, front_kills_mid_r, front_kills_mid_b
    #-----------------------------------------------------------------------
    #                               Top
    #-----------------------------------------------------------------------
    
    ganks_of_top_mid_r = Marker(
    "Successful mid ganks by red top",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            x[1][u'victimId'] == PID[TEAM.B_MID] and\
            (PID[TEAM.R_TOP] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.R_TOP] == x[1][u'killerId']), lambda x: False)
    )
    
    ganks_of_top_bot_r = Marker(
    "Successful bot ganks by red top",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            (x[1][u'victimId'] == PID[TEAM.B_ADC] or x[1][u'victimId'] == PID[TEAM.B_SUPP]) and\
            (PID[TEAM.R_TOP] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.R_TOP] == x[1][u'killerId']), lambda x: False)
    )
    
    ganks_of_top_mid_b = Marker(
    "Successful mid ganks by blue top",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            x[1][u'victimId'] == PID[TEAM.R_MID] and \
            (PID[TEAM.B_TOP] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.B_TOP] == x[1][u'killerId']), lambda x: False)
    )
    
    ganks_of_top_bot_b = Marker(
    "Successful bot ganks by blue top",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            (x[1][u'victimId'] == PID[TEAM.R_ADC] or x[1][u'victimId'] == PID[TEAM.R_SUPP]) and\
            (PID[TEAM.B_TOP] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.B_TOP] == x[1][u'killerId']), lambda x: False)
    )
    
    front_kills_top_r = Marker(
    "Front kills by red top",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            (x[1][u'victimId'] == PID[TEAM.B_TOP]) and\
            (PID[TEAM.R_TOP] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.R_TOP] == x[1][u'killerId']), lambda x: False)
    )
    
    front_kills_top_b = Marker(
    "Front kills by blue top",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            (x[1][u'victimId'] == PID[TEAM.R_TOP]) and\
            (PID[TEAM.B_TOP] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.B_TOP] == x[1][u'killerId']), lambda x: False)
    )
    
    indicators += ganks_of_top_mid_r, ganks_of_top_bot_r, ganks_of_mid_top_b,\
                  ganks_of_mid_bot_b, front_kills_top_r, front_kills_top_b
    
    #-----------------------------------------------------------------------
    #                               ADC
    #-----------------------------------------------------------------------
    
    ganks_of_adc_top_r = Marker(
    "Successful top ganks by red adc",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            x[1][u'victimId'] == PID[TEAM.B_TOP] and\
            (PID[TEAM.R_ADC] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.R_ADC] == x[1][u'killerId']), lambda x: False)
    )
    
    ganks_of_adc_mid_r = Marker(
    "Successful mid ganks by red adc",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            x[1][u'victimId'] == PID[TEAM.B_MID] and\
            (PID[TEAM.R_ADC] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.R_ADC] == x[1][u'killerId']), lambda x: False)
    )
    
    ganks_of_adc_top_b = Marker(
    "Successful top ganks by blue adc",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            x[1][u'victimId'] == PID[TEAM.R_TOP] and\
            (PID[TEAM.B_ADC] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.B_ADC] == x[1][u'killerId']), lambda x: False)
    )
    
    ganks_of_adc_mid_b = Marker(
    "Successful mid ganks by blue adc",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            x[1][u'victimId'] == PID[TEAM.R_MID] and\
            (PID[TEAM.B_ADC] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.B_ADC] == x[1][u'killerId']), lambda x: False)
    )
    
    front_kills_bot_b = Marker(
    "front bot kills by blue team",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            (x[1][u'victimId'] == PID[TEAM.R_ADC] or x[1][u'victimId'] == PID[TEAM.R_SUPP]) and\
            (PID[TEAM.B_ADC] in x[1][u'assistingParticipantIds'] or PID[TEAM.B_SUPP] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.B_ADC] == x[1][u'killerId'] or PID[TEAM.B_SUPP] == x[1][u'killerId']), lambda x: False)
    )
    
    front_kills_bot_r = Marker(
    "front bot kills by red team",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            (x[1][u'victimId'] == PID[TEAM.B_ADC] or x[1][u'victimId'] == PID[TEAM.B_SUPP]) and\
            (PID[TEAM.R_ADC] in x[1][u'assistingParticipantIds'] or PID[TEAM.R_SUPP] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.R_ADC] == x[1][u'killerId'] or PID[TEAM.R_SUPP] == x[1][u'killerId']), lambda x: False)
    )
    
    indicators += ganks_of_adc_top_r, ganks_of_adc_mid_b, ganks_of_adc_top_b,\
                  ganks_of_adc_mid_b, front_kills_bot_b, front_kills_bot_r
    
    #-----------------------------------------------------------------------
    #                               Support
    #-----------------------------------------------------------------------
    ganks_of_supp_top_r = Marker(
    "Successful top ganks by red supp",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            x[1][u'victimId'] == PID[TEAM.B_TOP] and\
            (PID[TEAM.R_SUPP] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.R_SUPP] == x[1][u'killerId']), lambda x: False)
    )
    
    ganks_of_supp_mid_r = Marker(
    "Successful mid ganks by red supp",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            x[1][u'victimId'] == PID[TEAM.B_MID] and\
            (PID[TEAM.R_SUPP] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.R_SUPP] == x[1][u'killerId']), lambda x: False)
    )
    
    ganks_of_supp_top_b = Marker(
    "Successful bot ganks by blue top",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            x[1][u'victimId'] == PID[TEAM.R_TOP] and\
            (PID[TEAM.B_SUPP] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.B_SUPP] == x[1][u'killerId']), lambda x: False)
    )
    
    ganks_of_supp_mid_b = Marker(
    "Successful mid ganks by blue supp",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
            x[1][u'victimId'] == PID[TEAM.R_MID] and\
            (PID[TEAM.B_SUPP] in x[1][u'assistingParticipantIds'] or 
            PID[TEAM.B_SUPP] == x[1][u'killerId']), lambda x: False)
    )
    
    indicators += ganks_of_supp_top_r, ganks_of_supp_mid_b, ganks_of_supp_top_b,\
                  ganks_of_supp_mid_b
    
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
    
    early_kills_by_r = Marker(
    "early kills by red team",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and ROLE[x[1][u'victimId']] in TEAM_B,
                      lambda x: False)
    )
    early_kills_by_b = Marker(
    "early kills by blue team",
    Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
    Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and ROLE[x[1][u'victimId']] in TEAM_R,
                      lambda x: False)
    )
    
    indicators += [peeling, early_kills_by_r, early_kills_by_b]
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
    
