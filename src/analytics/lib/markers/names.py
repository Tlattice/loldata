class names(object):
    def __init__(self):
        pass
    def __setattr__(self, name, value):
        self.__dict__[name] = value
    def __getattr__(self, key):
        return self.__dict__[key]
    def __setitem__(self, key, value):
        self.__dict__[key] = value
        self.__dict__[key+'_default'] = value
    def reset(self):
        for key in self.__dict__:
            if not '_default' in key:
                self.__dict__[key] = self.__dict__[key+'_default']
