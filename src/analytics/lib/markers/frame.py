from enum import Enum

class TYPE(Enum):
    PLAYER_STAT = "PLAYER_STAT"
    ITEM_PURCHASED = "ITEM_PURCHASED"
    SKILL_LEVEL_UP = "SKILL_LEVEL_UP"
    WARD_PLACED = "WARD_PLACED"
    ITEM_DESTROYED = "ITEM_DESTROYED"
    CHAMPION_KILL = "CHAMPION_KILL"
    ELITE_MONSTER_KILL = "ELITE_MONSTER_KILL"
    TOWER_BUILDING = "TOWER_BUILDING"
    BUILDING_KILL = "BUILDING_KILL"
    ITEM_UNDO = "ITEM_UNDO"
    WARD_KILL = "WARD_KILL"
    ITEM_SOLD = "ITEM_SOLD"

class FrameWrapper(dict):
    def __getattr__(self, key):
        try:
            if type(self[key]) == dict:
                return FrameWrapper(self[key])
            else:
                return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return '<DictX ' + dict.__repr__(self) + '>'

class FrameIterator:
    def __init__(self, frame):
        self.frame = frame.frame
        self.index = 0
    def __next__(self):
        if self.index < len(self.frame[u'events']):
            event = self.frame[u'events'][self.index]
            self.index += 1
            #return [TYPE(event[u'type']), event]
            return FrameWrapper({'type': TYPE(event[u'type']), 'payload' :event})
        elif self.index < len(self.frame[u'events'])+len(self.frame[u'participantFrames']):
            timestamp = self.frame[u'timestamp']
            pframe = self.frame[u'participantFrames'][str(self.index-len(self.frame[u'events'])+1)]
            pframe[u'timestamp'] = timestamp
            if not u'position' in pframe:
                pframe[u'position'] = {}
                pframe[u'position'][u'x'] = 0
                pframe[u'position'][u'y'] = 0
            self.index += 1
            #return [TYPE(u'PLAYER_STAT'), pframe]
            return FrameWrapper({'type': TYPE(u'PLAYER_STAT'), 'payload' :pframe})
        else:
            raise StopIteration

class Frames:
    def __init__(self, frame):
        self.frame = frame
    def __iter__(self):
        return FrameIterator(self)
