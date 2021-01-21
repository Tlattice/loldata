from markers.counters import *
from markers.frame import *
from markers.players import *
from markers.areas import *
from markers.names import *
from dynamic_model.rift import *
import os
import json
import configparser
from tqdm import tqdm
import numpy
import pymongo


# Paths
MATCH_PATH = 'output/match/'
TIMELINE_PATH = 'output/time/'

# Read and create markers
config = configparser.ConfigParser()
config.read('input/markers.ini')

dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
playsdb = dbclient["plays"]
matchescollection = playsdb["matches"]
timescollection = playsdb["timelines"]
matches = matchescollection.find({})
times = timescollection.find({})


# Check if the program is set verbose
VERBOSE = False
# ----------------------------------------------------------------------
#                      Create memory structures
# ----------------------------------------------------------------------
# All memories will be referenced using:
# mem.name_of_the_memory.attribute [= value_to_be_assigned]
# And created with:
# mem_name_of_my_memory
class global_memory:
    def __init__(self):
        self.inner_dict = {}
    def __getattr__(self, key):
        return self.inner_dict[key]
    def __setitem__(self, key, value):
        self.inner_dict[key] = value
    def reset(self):
        for value in self.inner_dict.values():
            value.reset()
            
mem = global_memory()
rift = Rift()
area = Area()
team = Team()
mks = [[] for i in range(10)]

class MarkerTemplate:
    def __init__(self, other = None):
        if other is None:
            self.l = []
        else:
            self.l = list(other.l)
    def append(self, x):
        self.l.append(x)
    def replace(self, a, b):
        res = False
        for i in range(len(self.l)):
            if a in self.l[i]:
                #print(a)
                #print(b)
                #print(self.l[i])
                self.l[i] = self.l[i].replace(a, str(b))
                #print(self.l[i])
                res = True
        return res
    def iter(self):
        return self.l

# ----------------------------------------------------------------------
#                         Loading init file
# ----------------------------------------------------------------------
templates = [] # holds the code templates
for name in config:
    if name == 'DEFAULT':
        continue
    if name == 'CONFIG':
        print("Found configuration section")
        section = config['CONFIG']
        VERBOSE = section.getboolean('VERBOSE', fallback=False)
        print("Verbose set to "+str(VERBOSE))
        continue
    prefix, spacename = name.split('.')
    if prefix == 'mem':
        print("- Creating memory: "+name[4:])
        nspace = names()
        mem[spacename] = nspace
        for attr in config[name]:
            typeword, indentifier = attr.split(' ')
            if typeword == 'int':
                print("-- Putting int attribute")
                value = config[name].getint(attr)
                nspace[indentifier] = value
            elif typeword == 'bool':
                print("-- Putting bool attribute")
                value = config[name].getboolean(attr)
                nspace[indentifier] = value
            elif typeword == 'str':
                print("-- Putting str attribute")
                value = config[name].get(attr)
                nspace[indentifier] = value
            elif typeword == 'float':
                print("-- Putting float attribute")
                value = float(config[name].get(attr))
                nspace[indentifier] = value
            else:
                print("Type not recognized: "+attr[:4])
        continue
    if prefix == 'mk':
        marker = MarkerTemplate()
        print("- Creating marker: "+name[3:])
        description = ''
        for attr in config[name]:
            if attr == 'description':
                print("-- Adding description")
                description = config[name][attr]
                marker.append(description)
            elif attr == 'start_condition':
                print("-- Adding start description")
                marker.append("def startcondition(f):"+config[name][attr].replace("$", " "))
            elif attr == 'stop_condition':
                print("-- Adding stop description")
                marker.append("def stopcondition(f):"+config[name][attr].replace("$", "  "))
            elif attr == 'count_policy':
                print("-- Adding count policy")
                marker.append("def countpolicy(f, c):\n"+config[name][attr].replace("$", "   "))
            else:
                print("Error: Non-recognized parameter")
        templates.append(marker)
        continue


# ----------------------------------------------------------------------
#                         Creating markers
# ----------------------------------------------------------------------
config_iter = {
'blue': [list(range(1, 6)), range(6, 11)],
'red': [range(6, 11), range(1, 6)]
}
timeslices = [(0, 5), (5, 10), (10, 15), (15, 20), (20, 25), (25, 30), (30, 35), (35, 40), (40, 45)]
for code in templates:
    # @player, @enemy, @ally, @team, @from, @to
    # e.g: rift.@team.mid.position
    for tteam in config_iter:
        playerteam = config_iter[tteam][0]
        enemyteam = config_iter[tteam][1]
        teamcode = MarkerTemplate(code)
        ainteam = code.replace('@team', tteam)
        for player in playerteam:
            player_markers = []
            playercode = MarkerTemplate(teamcode)
            ainplayer = playercode.replace('@player', TEAM_DICT[player])
            for fromtime, totime in timeslices:
                timecode = MarkerTemplate(playercode)
                ainfrom = timecode.replace('@from', fromtime)
                ainto = timecode.replace('@to', totime)
                slicedmarkers = []
                for enemy in enemyteam:
                    enemycode = MarkerTemplate(timecode)
                    ainenemy = enemycode.replace('@enemy', TEAM_DICT[enemy])
                    for ally in playerteam:
                        allycode = MarkerTemplate(enemycode)
                        ainally = allycode.replace('@ally', TEAM_DICT[ally])
                        l = allycode.iter()
                        description = l[0]
                        exec(l[1])
                        exec(l[2])
                        exec(l[3])
                        slicedmarkers.append(Marker(description, Trigger(startcondition, stopcondition), Counter(countpolicy)))
                        if not ainally:
                            break
                    if not ainenemy:
                        break
                if not (ainto or ainfrom):
                    break
                player_markers.append(slicedmarkers)
            mks[player-1] += player_markers
            if not ainplayer:
                break
# ----------------------------------------------------------------------
#                         Applying markers
# ----------------------------------------------------------------------
filenames = []
results = {}

for timeline in tqdm(times):
    # Game stats
    try:
        if(len(timeline[u'frames']) < 6):
            print("Team surrendered")
            continue
        ROLE = map_players_by_point({}, [frame[u'participantFrames'] for frame in timeline[u'frames'][1:8]])
    except Exception as e:
        print("Error reading frames")
        print(e)
        continue
    PID = get_PID(ROLE)
    try:
        for raw_frames in timeline[u'frames']:
            for frame in Frames(raw_frames):
                rift(frame)
                #Single-threaded version
                for marker in mks:
                    marker(frame)
    except Exception as e:
        print("Error when executing a marker")
        print(e)
        continue
    # Save results
    gid = '1234'
    #for indexplayer in range(len(mks)):
    #    results[gid][indexplayer][indexslice][indexmarker] = mks[indexplayer][indexslice][indexmarker].count()
    #    mks[indexplayer][indexslice][indexmarker].reset()
    #for marker in mks:
    #    results[gid].append(marker.count())
    #    marker.reset()
    mem.reset()
    rift.clean()
    print(results)

print("Saving results...")
with open('output/results.json', 'w') as f:
    json.dump(results, f)
