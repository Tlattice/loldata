import wget
import json
import requests
import urllib
import time
import os.path

MATCH_PATH = '../match'
TIMELINE_PATH = '../time'

KEY = 'RGAPI-12524fad-25b9-4875-b2c3-614656f2c05c'

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
        #self.account_id = account_id
        url = ID_BY_NAME.format(self.region, name, self.key)
        response = json.loads(requests.get(url).text)
        self.account_ids.add( response[u'accountId'] )
        
    def save_id(self, name=''):
        self.__get_account_id(name)
        
    def __get_match_list(self, account_id='', depth = 4):
        if account_id:
            account_id = self.account_id
        url = MATCHLIST_BY_ACCOUNTID.format(self.region, self.account_id, 420, self.key)
        response = json.loads(requests.get(url).text)
        if u'status' in response:
            return set()
        z = [x[u'gameId'] for x in response[u'matches']]
        return set(z[:depth])
    
    def __get_match_info(self, matchid):
        url = MATCH_BY_ID.format(self.region, matchid, self.key)
        filename = str(matchid)+'.json'
        urllib.urlretrieve(url, filename=filename)
        with open(filename) as file:
            data = json.loads(file.read())
        if u'status' in data:
            return set()
        return {x[u'player'][u'accountId'] for x in data[u'participantIdentities']}
    
    def __get_match_timeline(self, matchid):
        url = MATCH_TIMELINE_BY_ID.format(self.region, matchid, self.key)
        filename = str(matchid)+'_timeline.json'
        urllib.urlretrieve(url, filename=filename)
        
    def run(self):
        counter = 0
        while self.account_ids and counter < self.max_summoners:
            self.account_id = account_id = self.account_ids.pop()
            self.match_list = self.__get_match_list(account_id, self.depth).difference( self.filtered_matches )
            print self.filtered_matches
            self.filtered_matches = self.filtered_matches.union(self.match_list)
            time.sleep(1)
            for match in self.match_list:
                summoners = self.__get_match_info(match); # Saves the match
                if summoners:
                    self.__get_match_timeline(match); # Saves timeline
                self.account_ids = self.account_ids.union(summoners.difference(self.filtered_ids))
                #self.filtered_ids = self.account_ids
                time.sleep(1)
            counter += 1
            
rf = RiotFetcher('la1', KEY, 99999999, 10)
rf.save_id('Bow')
rf.run()
