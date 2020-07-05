from timeline.counters import *
from timeline.frame import *
from timeline.players import *
from timeline.areas import *

from scipy.spatial.distance import cdist
import json

MATCH_CONST = 'data/match_info.json'
FRAME_CONST = 'data/frame_info.json'
with open(MATCH_CONST) as file:
    match = json.loads(file.read())
with open(FRAME_CONST) as file:
    framed = json.loads(file.read())

map_players(match[u'participants'])
PID = get_PID()

#-----------------------------------------------------------------------
#                               Markers
#-----------------------------------------------------------------------
indicators = []
#-----------------------------------------------------------------------
#                               Jungle
#-----------------------------------------------------------------------
# How many times the jungle came and help some line before destroying a
# tower.
sucessful_ganks_r = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and
        (PID[TEAM.R_JG] in x[1][u'assistingParticipantIds'] or 
        PID[TEAM.R_JG] == x[1][u'killerId']), lambda x: False)
)
sucessful_ganks_b = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and
        (PID[TEAM.B_JG] in x[1][u'assistingParticipantIds'] or 
        PID[TEAM.B_JG] == x[1][u'killerId']), lambda x: False)
)

harassment_blue = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.PLAYER_STAT and \
        ROLE[x[1][u'participantId']]==TEAM.R_JG and \
        INBLUEJG( (x[1][u'position'][u'x'], x[1][u'position'][u'y']) ),
        lambda x: False)
)

harassment_red = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.PLAYER_STAT and \
        ROLE[x[1][u'participantId']]==TEAM.B_JG and \
        INREDJG( (x[1][u'position'][u'x'], x[1][u'position'][u'y']) ),
        lambda x: False)
)

time = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.PLAYER_STAT and \
        ROLE[x[1][u'participantId']]==TEAM.B_JG,
        lambda x: False)
)

indicators += sucessful_ganks_r, sucessful_ganks_b, harassment_blue, \
              harassment_red, time
# 
#-----------------------------------------------------------------------
#                               Middle
#-----------------------------------------------------------------------
ganks_of_mid_top_r = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
        x[1][u'victimId'] == PID[TEAM.B_TOP] and\
        (PID[TEAM.R_MID] in x[1][u'assistingParticipantIds'] or 
        PID[TEAM.R_MID] == x[1][u'killerId']), lambda x: False)
)

ganks_of_mid_bot_r = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
        (x[1][u'victimId'] == PID[TEAM.B_ADC] or x[1][u'victimId'] == PID[TEAM.B_SUPP]) and\
        (PID[TEAM.R_MID] in x[1][u'assistingParticipantIds'] or 
        PID[TEAM.R_MID] == x[1][u'killerId']), lambda x: False)
)

ganks_of_mid_top_b = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
        x[1][u'victimId'] == PID[TEAM.R_TOP] and \
        (PID[TEAM.B_MID] in x[1][u'assistingParticipantIds'] or 
        PID[TEAM.B_MID] == x[1][u'killerId']), lambda x: False)
)

ganks_of_mid_bot_b = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
        (x[1][u'victimId'] == PID[TEAM.R_ADC] or x[1][u'victimId'] == PID[TEAM.R_SUPP]) and\
        (PID[TEAM.B_MID] in x[1][u'assistingParticipantIds'] or 
        PID[TEAM.B_MID] == x[1][u'killerId']), lambda x: False)
)

indicators += ganks_of_mid_top_r, ganks_of_mid_bot_r, ganks_of_mid_top_b,\
              ganks_of_mid_bot_b
#-----------------------------------------------------------------------
#                               Top
#-----------------------------------------------------------------------

ganks_of_top_mid_r = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
        x[1][u'victimId'] == PID[TEAM.B_MID] and\
        (PID[TEAM.R_TOP] in x[1][u'assistingParticipantIds'] or 
        PID[TEAM.R_TOP] == x[1][u'killerId']), lambda x: False)
)

ganks_of_top_bot_r = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
        (x[1][u'victimId'] == PID[TEAM.B_ADC] or x[1][u'victimId'] == PID[TEAM.B_SUPP]) and\
        (PID[TEAM.R_TOP] in x[1][u'assistingParticipantIds'] or 
        PID[TEAM.R_TOP] == x[1][u'killerId']), lambda x: False)
)

ganks_of_top_mid_b = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
        x[1][u'victimId'] == PID[TEAM.R_MID] and \
        (PID[TEAM.B_TOP] in x[1][u'assistingParticipantIds'] or 
        PID[TEAM.B_TOP] == x[1][u'killerId']), lambda x: False)
)

ganks_of_top_bot_b = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
        (x[1][u'victimId'] == PID[TEAM.R_ADC] or x[1][u'victimId'] == PID[TEAM.R_SUPP]) and\
        (PID[TEAM.B_TOP] in x[1][u'assistingParticipantIds'] or 
        PID[TEAM.B_TOP] == x[1][u'killerId']), lambda x: False)
)

indicators += ganks_of_top_mid_r, ganks_of_top_bot_r, ganks_of_mid_top_b,\
              ganks_of_mid_bot_b

#-----------------------------------------------------------------------
#                               ADC
#-----------------------------------------------------------------------

ganks_of_adc_top_r = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
        x[1][u'victimId'] == PID[TEAM.B_TOP] and\
        (PID[TEAM.R_ADC] in x[1][u'assistingParticipantIds'] or 
        PID[TEAM.R_ADC] == x[1][u'killerId']), lambda x: False)
)

ganks_of_adc_mid_r = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
        x[1][u'victimId'] == PID[TEAM.B_MID] and\
        (PID[TEAM.R_ADC] in x[1][u'assistingParticipantIds'] or 
        PID[TEAM.R_ADC] == x[1][u'killerId']), lambda x: False)
)

ganks_of_adc_top_b = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
        x[1][u'victimId'] == PID[TEAM.R_TOP] and\
        (PID[TEAM.B_ADC] in x[1][u'assistingParticipantIds'] or 
        PID[TEAM.B_ADC] == x[1][u'killerId']), lambda x: False)
)

ganks_of_adc_mid_b = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
        x[1][u'victimId'] == PID[TEAM.R_MID] and\
        (PID[TEAM.B_ADC] in x[1][u'assistingParticipantIds'] or 
        PID[TEAM.B_ADC] == x[1][u'killerId']), lambda x: False)
)

indicators += ganks_of_adc_top_r, ganks_of_adc_mid_b, ganks_of_adc_top_b,\
              ganks_of_adc_mid_b

#-----------------------------------------------------------------------
#                               Support
#-----------------------------------------------------------------------
ganks_of_supp_top_r = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
        x[1][u'victimId'] == PID[TEAM.B_TOP] and\
        (PID[TEAM.R_SUPP] in x[1][u'assistingParticipantIds'] or 
        PID[TEAM.R_SUPP] == x[1][u'killerId']), lambda x: False)
)

ganks_of_supp_mid_r = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
        x[1][u'victimId'] == PID[TEAM.B_MID] and\
        (PID[TEAM.R_SUPP] in x[1][u'assistingParticipantIds'] or 
        PID[TEAM.R_SUPP] == x[1][u'killerId']), lambda x: False)
)

ganks_of_supp_top_b = Marker(
Trigger(lambda f: f[1][u'timestamp'] == 0, lambda f: f[0] == TYPE.BUILDING_KILL),
Counter(lambda x: x[0] == TYPE.CHAMPION_KILL and \
        x[1][u'victimId'] == PID[TEAM.R_TOP] and\
        (PID[TEAM.B_SUPP] in x[1][u'assistingParticipantIds'] or 
        PID[TEAM.B_SUPP] == x[1][u'killerId']), lambda x: False)
)

ganks_of_supp_mid_b = Marker(
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
# Number of times that died at some place

class peel_stack:
    def __init__(self):
        self.labels = []
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
Trigger(lambda f: f[0] == TYPE.PLAYER_STAT,
        lambda f: ps.peel_pop( f[0] != TYPE.PLAYER_STAT) ),
Counter( lambda x: ps(x[1][u'position'], ROLE[x[1][u'participantId']]),
         lambda x: False)
)

indicators += [peeling]

#-----------------------------------------------------------------------
#                               Main
#-----------------------------------------------------------------------
for d in framed[u'frames']:
    for f in Frame(d):
        for ind in indicators:
            ind(f)
for ind in indicators:
    print(ind.count())
