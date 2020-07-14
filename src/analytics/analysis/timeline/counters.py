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
        """
        if self.start_condition(frame):
            self.capturing = True
        elif self.stop_condition(frame):
            self.capturing = False
        """
    def iscapturing(self):
        return self.capturing

class Counter:
    def __init__(self, add_cond, sub_cond, minbound = 0, maxbound = 9999):
        self.count = 0
        self.minbound = minbound
        self.maxbound = maxbound
        self.add_cond = add_cond
        self.sub_cond = sub_cond
    def __count_up(self):
        if self.count < self.maxbound:
            self.count += 1
            #print "count up!"
    def __count_down(self):
        if self.minbound < self.count:
            self.count -= 1
    def __call__(self, frame):
        if self.add_cond(frame):
            self.__count_up()
            return True
        elif self.sub_cond(frame):
            self.__count_down()
            return False
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

    def desc(self):
        return self.description

    def printl(self):
        print self.description
        print self.counter.getcount()
