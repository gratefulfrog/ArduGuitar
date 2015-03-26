#!/usr/local/bin/python3.4
# components.py
# provides classes for all physical components of the guitar
# 

from state import State

class CurrentNextable:
    """ this class provides the services for anything that 
    has a current and a next 'state' as in the class State.
    Note that the current and next values must be atomic, not
    structured objects! Otherwise it won't work due to copy
    vs. reference issues.
    """
    cur = 0
    nex = 1

    def __init__(self):
        self.cn = [State.off,State.off]
    
    def current(self):
        return self.cn[self.cur]

    def next(self):
        return self.cn[self.nex]
    
    def reset(self, nextt = True, current = False):
        if current:
            self.cn[CurrentNextable.cur] = State.off
        if nextt:
            self.cn[CurrentNextable.nex] = State.off

    def update(self, new,add=False):
        if not add or self.cn[self.nex] == None:
            self.cn[self.nex] = new
        else:
            self.cn[self.nex] += new

    def x(self):
        self.cn[self.cur] = self.cn[self.nex]

    def __repr__(self):
        return 'CurrentNextable: ' + '\n\t'  \
            'current:\t' + str(self.cn[CurrentNextable.cur]) +'\n\t' + \
            'next:\t' + str(self.cn[CurrentNextable.nex]) 


class Connectable:
    """ anything which connects.
    Note that the connection is represented as a pair:
    (poleId, poilPolePair) eg. 0 -> ('B',1)
    The name of the connector is not held in this class but
    is required in the subclasses.
    """
    def __init__(self):
        self.connected2 = [CurrentNextable(),CurrentNextable()]
        self.reset = True

    def resetNextConnections(self):
        for i in (0,1):
            self.connected2[i].reset()
        self.reset = True

    #def connect(self, myPoleId, coilPolePair):
    def connect(self, myPoleId, coilPolePairAsList):
        appendNew = True
        if (not self.reset):
            self.resetNextConnections()
            appendNew = False
        #self.connected2[myPoleId].update((coilPolePair,), add = appendNew)
        self.connected2[myPoleId].update([coilPolePairAsList,], add = appendNew)
    
    def x(self):
        for c in self.connected2:
            if (not c == None):
                c.x() 
        self.reset = False

    def __repr__(self):
        return 'Connectable:\n\t' + \
            'reset:\t' + str(self.reset) + '\n\t' + \
            'Connected2:\n\t\t' + \
            str(self.connected2[0]).replace('\n','\n\t') + '\n\t\t' + \
            str(self.connected2[1]).replace('\n','\n\t')

class VTable(Connectable):    
    """Providing services for anything with a Volume, Tone, and ToneRange.
    The name is needed for connection purposes.
    """
    def __init__(self,name):
        Connectable.__init__(self)
        self.name = name
        self.vol_ = CurrentNextable()
        self.tone_  = CurrentNextable()
        self.toneRange_  = CurrentNextable()

    def vol(self,level):
        self.vol_.update(level)

    def tone(self,level):
        self.tone_.update(level)

    def toneRange(self,level):
        self.toneRange_.update(level)

    def x(self):
        self.vol_.x()
        self.tone_.x()
        self.toneRange_.x()
        super().x()

    def __repr__(self):
        return '\nVTable: ' + self.name + '\n\t' + \
            'vol: ' + str(self.vol_) + '\n\t' +\
            'tone: ' + str(self.tone_) + '\n\t' + \
            'toneRange: ' + str(self.toneRange_) + '\n\t' + \
            super().__repr__().replace('\n','\n\t')
            
class Invertable(VTable):    
    """Providing services for anything which cna be intervert.
    The name is passed to the superclass!
    """
    def __init__(self,name):
        VTable.__init__(self,name)
        self.invert_ = CurrentNextable()

    def invert(self,level):
        self.invert_.update(level)

    def x(self):
        self.invert_.x()
        super().x()

    def __repr__(self):
        return '\nInvertable:\n\t' + \
            'invert: ' + str(self.invert_) + '\n\t' +\
            super().__repr__().replace('\n','\n\t')

        
