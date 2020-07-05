from enum import Enum

class TEAM(Enum):
    B_TOP = 0
    B_MID = 1
    B_ADC = 2
    B_SUPP = 3
    B_JG = 4
    R_TOP = 5
    R_MID = 6
    R_ADC = 7
    R_SUPP = 8
    R_JG = 9

# Usage: PARTICIPANTID[TEAMRED.JG] -> 12
PARTICIPANTID = [-1 for i in range(11)]
# Usage: ROLE[id] -> TEAM.R_TOP
ROLE = {}

def map_players(participants):
    for frame in participants:
        lane = frame[u'timeline'][u'lane']
        role = frame[u'timeline'][u'role']
        pid = frame[u'participantId']
        team = 0 if frame[u'teamId']==100 else 5
        if lane=='TOP':
            ROLE[pid] = TEAM(team + 0)
        elif lane=='JUNGLE':
            ROLE[pid] = TEAM(team + 4)
        elif lane=='MIDDLE':
            ROLE[pid] = TEAM(team + 1)
        elif lane=='BOTTOM':
            if role == 'DUO_CARRY':
                ROLE[pid] = TEAM(team + 2)
            elif role == 'DUO_SUPPORT':
                ROLE[pid] = TEAM(team + 3)

def get_PID():
    return {v: k for k, v in ROLE.iteritems()}
