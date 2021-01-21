import wget
import json
import requests
import urllib.request
import time
import os.path
#import urllib.request as urllib
import pymongo

GAME_TYPE = 420

DELAY = 0.8

dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
nplaysdb = dbclient["nplays"]
cmatches = nplaysdb["matches"]
ctimes = nplaysdb["timelines"]
csummoners = nplaysdb["summoners"]
clist = nplaysdb["list"]

#MATCH_PATH = 'output/match/'
#TIMELINE_PATH = 'output/time/'

with open('input/rra.key', 'rb') as f:
    KEY = f.readline().decode('utf-8')

#Get account-id
ID_BY_NAME = \
"https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}"

#Get a match list
MATCHLIST_BY_ACCOUNTID = \
"https://{}.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?queue={}&api_key={}"

#Get match information
MATCH_BY_ID= \
"https://{}.api.riotgames.com/lol/match/v4/matches/{}?api_key={}"

#Get match timeline
MATCH_TIMELINE_BY_ID = \
"https://{}.api.riotgames.com/lol/match/v4/timelines/by-match/{}?api_key={}"

# Pipeline
# get account id for summoner name
# get match list by account id
# get match information
# get match timeline

class RiotFetcher:
    def __init__(self, region='na', key='', max_summoners = 4, depth = 3):
        # Configuration constants
        self.region = region
        self.key = key
        self.depth = depth
        self.account_id = ''
        
        # Execution variables
        self.max_summoners = max_summoners
        
        # Pipeline variables
        #   Summoners pending to be checked
        self.account_ids = set()
        #   Summoners already checked
        self.filtered_ids = set()
        #   Matches to be checked
        self.match_list = set()
        #   Matches already checked
        self.filtered_matches = set()
        
    def __get_account_id(self, name=''):
        if not name:
            print("Error: name required.")
        self.name = name
        print("Getting account id: "+ name)
        url = ID_BY_NAME.format(self.region, name, self.key)
        response = json.loads(requests.get(url).text)
        # Insert data into the collection
        csummoners.insert_one(response)
        try:
            self.account_ids.add( response[u'accountId'] )
        except:
            print("No accountId found.")
        time.sleep(DELAY)
        
    def save_id(self, name=''):
        self.__get_account_id(name)
        
    def __get_match_list(self, account_id='', depth = 4):
        if account_id:
            account_id = self.account_id
        url = MATCHLIST_BY_ACCOUNTID.format(self.region, self.account_id, GAME_TYPE, self.key)
        print("Retrieving match list: {}".format(account_id))
        response = json.loads(requests.get(url).text)
        time.sleep(DELAY)
        if u'status' in response:
            print("Error retrieving match list.")
            return set()
        time.sleep(DELAY)
        z = [x[u'gameId'] for x in response[u'matches']]
        return set(z[:depth])
    
    def __get_match_info(self, matchid, post_id):
        url = MATCH_BY_ID.format(self.region, matchid, self.key)
        filename = str(matchid)+'.json'
        response = cmatches.find_one({'matchId': matchid})
        if response:
            print("Match found: {}".format(matchid))
        else:
            print("Downloading match: {}".format(filename))
            urllib.request.urlretrieve(url, filename)
            response = json.loads(requests.get(url).text)
            response['matchId'] = matchid
            response['timelineId'] = post_id
            # Insert match into the database
            cmatches.insert_one(response)
            time.sleep(DELAY)
        if u'status' in response:
            print("Status error. Skipping.")
            return set()
        return {x[u'player'][u'accountId'] for x in response[u'participantIdentities']}
    
    def __get_match_timeline(self, matchid):
        url = MATCH_TIMELINE_BY_ID.format(self.region, matchid, self.key)
        filename = str(matchid)+'_timeline.json'
        response = ctimes.find_one({'matchId': matchid})
        if response:
            print("Timeline found: {}".format(filename))
            return response['_id']
        else:
            print("Downloading timeline: {}".format(filename))
            urllib.request.urlretrieve(url, filename)
            response = json.loads(requests.get(url).text)
            response['matchId'] = matchid
            post_id = ctimes.insert_one(response).inserted_id
            time.sleep(DELAY)
            return(post_id)
        
    def run(self):
        counter = 0
        while self.account_ids and counter < self.max_summoners:
            self.account_id = account_id = self.account_ids.pop()
            self.match_list = self.__get_match_list(account_id, self.depth).difference( self.filtered_matches )
            self.filtered_matches = self.filtered_matches.union(self.match_list)
            for match in self.match_list:
                post_id = self.__get_match_timeline(match); # Saves timeline
                summoners = self.__get_match_info(match, post_id); # Saves the match
                #if summoners:
                #    self.__get_match_timeline(match); # Saves timeline
                self.account_ids = self.account_ids.union(summoners.difference(self.filtered_ids))
            counter += 1
            
rf = RiotFetcher('la1', KEY, 99999999, 3)
print("Loading initial conditions:")
with open('input/summonerstofetch.init', 'rb') as f:
    summoners = f.readlines()
    for summoner in summoners:
        name = summoner.decode('utf-8')[:-1]
        print("Adding "+name)
        rf.save_id(name)
rf.run()
