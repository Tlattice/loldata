import wget
import json
import urllib.request

MATCH_PATH = ''
TIMELINE_PATH = ''

#Get account-id
ID_BY_NAME = \
"https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}"

#Get a match list
MATCHLIST_BY_ACCOUNTID = \
"https://{}.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?api_key={}"

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
        
        # Execution variables
        self.max_summoners = max_summoners
        
        # Pipeline variables
        #   Summoners pending to be checked
        self.account_ids = []
        #   Summoners already checked
        self.filtered_ids = []
        #   Matches to be checked
        self.match_list = []
        #   Matches already checked
        self.filtered_matches = []
        
    def __get_account_id(self, name=''):
        if not name:
            print("Error: name required.")
        self.name = name
        self.account_id = account_id
        url = ID_BY_NAME.format(self.region, name, self.key)
        wget.download(url, bar=bar_thermometer)
        
    def __get_match_list(self, account_id=''):
        if account_id:
            account_id = self.account_id
        url = MATCHLIST_BY_ACCOUNTID.format(self.region, self.account_id, self.key)
        wget.download(url, bar=bar_thermometer)
        # Cut by depth
    
    def run(self):
        counter = 0
        while account_ids and counter < self.max_summoners:
            account_id = account_ids.pop(0)
            self.match_list = self.__get_match_list(account_id, self.depth)-self.filtered_matches
            self.filtered_matches = self.match_list
            for match in self.match_list:
                summoners = self.__get_match_info(match); # Saves the match
                self.__get_match_timeline(match); # Saves timeline
                self.account_ids += summoners-self.filtered_ids
                self.filtered_ids = self.account_ids
            counter += 1
            
