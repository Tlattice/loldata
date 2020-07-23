import wget
import json
import requests
import urllib
import time
import os.path
import urllib.request as urllib

MATCH_PATH = 'output/match/'
TIMELINE_PATH = 'output/time/'

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
        self.account_ids.add( response[u'accountId'] )
        time.sleep(1)
        
    def save_id(self, name=''):
        self.__get_account_id(name)
        
    def __get_match_list(self, account_id='', depth = 4):
        if account_id:
            account_id = self.account_id
        url = MATCHLIST_BY_ACCOUNTID.format(self.region, self.account_id, 420, self.key)
        print("Retrieving match list: {}".format(account_id))
        response = json.loads(requests.get(url).text)
        time.sleep(1)
        if u'status' in response:
            print("Error retrieving match list.")
            return set()
        time.sleep(1)
        z = [x[u'gameId'] for x in response[u'matches']]
        return set(z[:depth])
    
    def __get_match_info(self, matchid):
        url = MATCH_BY_ID.format(self.region, matchid, self.key)
        filename = str(matchid)+'.json'
        try:
            with open(MATCH_PATH+filename, 'rb') as f:
                pass
            print("Match found: {}".format(filename))
        except:
            print("Downloading match: {}".format(filename))
            urllib.urlretrieve(url, filename=MATCH_PATH+filename)
            time.sleep(1)
        with open(MATCH_PATH+filename) as fil:
            data = json.loads(fil.read())
        if u'status' in data:
            print("Status found. Skipping.")
            return set()
        return {x[u'player'][u'accountId'] for x in data[u'participantIdentities']}
    
    def __get_match_timeline(self, matchid):
        url = MATCH_TIMELINE_BY_ID.format(self.region, matchid, self.key)
        filename = str(matchid)+'_timeline.json'
        try:
            with open(TIMELINE_PATH+filename, 'rb') as f:
                pass
            print("Timeline found: {}".format(filename))
        except:
            print("Downloading timeline: {}".format(filename))
            urllib.urlretrieve(url, filename=TIMELINE_PATH+filename)
            time.sleep(1)
        
    def run(self):
        counter = 0
        while self.account_ids and counter < self.max_summoners:
            self.account_id = account_id = self.account_ids.pop()
            self.match_list = self.__get_match_list(account_id, self.depth).difference( self.filtered_matches )
            self.filtered_matches = self.filtered_matches.union(self.match_list)
            for match in self.match_list:
                summoners = self.__get_match_info(match); # Saves the match
                if summoners:
                    self.__get_match_timeline(match); # Saves timeline
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
