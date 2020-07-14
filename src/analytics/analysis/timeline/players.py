from enum import Enum
from timeline.areas import *

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

TEAM_B = [TEAM.B_ADC, TEAM.B_SUPP, TEAM.B_TOP, TEAM.B_MID, TEAM.B_JG]
TEAM_R = [TEAM.R_ADC, TEAM.R_SUPP, TEAM.R_TOP, TEAM.R_MID, TEAM.R_JG]

# Usage: PARTICIPANTID[TEAMRED.JG] -> 12
PARTICIPANTID = [-1 for i in range(11)]
# Usage: ROLE[id] -> TEAM.R_TOP
ROLE = {}

# pass it two or three frames
# participants from gameid.json
# participantFrames(at least 4) from gameid_timelines.json
def map_players_by_point(participants, participantFrames):
    global ROLE
    team = lambda x: 'blue' if x<6 else 'red'
    # TOP, MID, BOT JG
    pid = [{'champ':0, 'role': [0, 0, [0, 0], 0]} for i in range(11)]
    final = [0 for i in range(11)]
    def convert(l):
        r = {}
        index = 0
        for x in l:
            if 'blue' in x:
                t = 0
            else:
                t = 5
            if 'top' in x:
                r[index] = TEAM(t+0)
            elif 'mid' in x:
                r[index] = (TEAM(t+1))
            elif 'adc' in x:
                r[index] = (TEAM(t+2))
            elif 'supp' in x:
                r[index] = (TEAM(t+3))
            elif 'jg' in x:
                r[index] = (TEAM(t+4))
            index += 1
        return r
    def maxindex(l):
        #print l
        v = l[0]
        i = 0
        for j in range(1, len(l)):
            if type(l[j]) == list:
                if l[j][0] > v:
                    i = j
                    v = l[j][0]
            else:
                if l[j] > v:
                    i = j
                    v = l[j]
        return i
    for participant in participants:
        pid[participant[u'participantId']][u'champ'] = participant[u'championId']
    #print participantFrames
    for pf in participantFrames:
        for frame in pf.values():
            if not u'position' in frame:
                continue
            pos = [frame[u'position'][u'x'], frame[u'position'][u'y']]
            #print frame[u'participantId']
            #print pos
            if team(frame[u'participantId']) == 'red':
                pid[frame[u'participantId']]['role'][0] += 1 if INREDTOP(pos) else 0
                pid[frame[u'participantId']]['role'][1] += 1 if INREDMID(pos) else 0
                pid[frame[u'participantId']]['role'][2][0] += 1 if INREDBOT(pos) else 0
                pid[frame[u'participantId']]['role'][3] = 3*frame[u'jungleMinionsKilled']#1 if INREDJG(pos) else 0
            else:
                pid[frame[u'participantId']]['role'][0] += 1 if INBLUETOP(pos) else 0
                pid[frame[u'participantId']]['role'][1] += 1 if INBLUEMID(pos) else 0
                pid[frame[u'participantId']]['role'][2][0] += 1 if INBLUEBOT(pos) else 0
                pid[frame[u'participantId']]['role'][3] = 3*frame[u'jungleMinionsKilled']#1 if INBLUEJG(pos) else 0
            pid[frame[u'participantId']]['role'][2][1] = frame[u'minionsKilled']
    botlist = {'red':[], 'blue':[]}
    #print pid[1:]
    for i in range(1,len(pid)):
        t = pid[i]
        #print t
        #print "for: "
        #print t['role']
        #print t['role']
        role = maxindex(t['role'])
        #print role
        #print team(i)
        if role == 0:
            final[i] = team(i)+'_top'
        elif role == 1:
            final[i] = team(i)+'_'+'mid'
        elif role == 2:
            minions = t['role'][2][1]
            botlist[team(i)].append([i, minions])
        elif role == 3:
            #print "*************"
            final[i] = team(i)+'_'+'jg'
        else:
            print "An error!!!"
    sorted(botlist['red'], key=lambda x: x[1])
    sorted(botlist['blue'], key=lambda x: x[1])
    #print "botlist"
    #print botlist
    final[botlist['red'][-1][0]] = 'red_adc'
    final[botlist['red'][0][0]] = 'red_supp' 
    final[botlist['blue'][-1][0]] = 'blue_adc'
    final[botlist['blue'][0][0]] = 'blue_supp'
    #print final[1:]
    # Check that everything is good
    ch = {'blue_supp':0, 'blue_top':0, 'blue_mid':0, 'blue_jg':0, 'blue_adc':0, 'red_supp':0, 'red_top':0, 'red_mid':0, 'red_jg':0, 'red_adc':0}
    for i in range(len(final)):
        if i == 0:
            continue
        if type(final[i]) == int:
            print "changing-----------------------------------------------------"
            for c in ch:
                if not c in final:
                    final[i] = c
    print final[1:]
    return convert(final[1:])
            
    

def map_players(participants):
    global ROLE
    #ROLE = {}
    for frame in participants:
        lane = frame[u'timeline'][u'lane']
        role = frame[u'timeline'][u'role']
        pid = frame[u'participantId']
        team = 0 if frame[u'teamId']==100 else 5
        print lane+'_'+role
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

def get_PID(role_var={}):
    if not role_var:
        return {v: k for k, v in ROLE.iteritems()}
    else:
        return {v: k for k, v in role_var.iteritems()}

def champ_id_match(participants, role_var={}):
    x = {}
    for frame in participants:
        #print frame
        #print role_var
        pid = frame[u'participantId']-1
        champ = frame[u'championId']
        #print role_var[pid]
        x[role_var[pid]] = champ
    return x
