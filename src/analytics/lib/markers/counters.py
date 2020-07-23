class Trigger:
    def __init__(self, start_condition, stop_condition):
        self.start_condition = start_condition
        self.stop_condition = stop_condition
        self.capturing = False
    def __call__(self, frame):
        if self.capturing:
            if self.stop_condition(frame):
                self.capturing = False
        else:
            if self.start_condition(frame):
                self.capturing = True
    def iscapturing(self):
        return self.capturing

class Counter:
    def __init__(self, count_policy, memory = None):
        self.count = 0
        self.count_policy = count_policy
    def __call__(self, frame):
        self.count = self.count_policy(frame, self.count)
    def getcount(self):
        return self.count

class Marker:
    def __init__(self, description, trigger, counter):
        self.description = description
        self.trigger = trigger
        self.counter = counter
    def __call__(self, frame):
        self.trigger(frame)
        if self.trigger.iscapturing():
            return self.counter(frame)
    def count(self):
        return self.counter.getcount()
        
    def reset(self):
        self.counter.count = 0

    def desc(self):
        return self.description

    def printl(self):
        print(self.description)
        print(self.counter.getcount())
