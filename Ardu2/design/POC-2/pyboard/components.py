#!/usr/bin/python3
# components/py
# provides classes for all physical components of the guitar
# 

from state import *
#from ivtControl import *

class CurrentNextable:
    cur = 0
    next = 1

    def __init__(self):
        self.cn = [State.off,State.off]

    def update(self, new):
        self.cn[self.next] = new

    def x(self):
        self.cn[self.cur] = self.cn[self.next]

    def __repr__(self):
        return 'CurrentNextable: ' +  \
            str(self.cn)

class Connectable:
    def __init__(self, name, plusPole, minusPole):
        self.name = name
        self.poles = [plusPole, minusPole]
        self.connected2 = [CurrentNextable(),CurrentNextable()]

    def connect(self, myPoleId, otherPoleId):
        self.connected2[myPoleId%2].update(otherPoleId)    
    
    def x(self):
        for c in self.connected2:
            if (not c == None):
                c.x() 

    def __repr__(self):
        return 'Connectable: ' + self.name + '\n\t' + \
            'poles: ' + str(self.poles)  + '\n\t' + \
            'Connected2: ' + str(self.connected2)

class VTable(Connectable):    
    def __init__(self,name, plusPole, minusPole):
        Connectable.__init__(self,name,plusPole, minusPole)
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
        return 'VTable: ' + self.name + '\n\t' + \
            'vol: ' + str(self.vol_) + '\n\t' +\
            'tone: ' + str(self.tone_) + '\n\t' + \
            'toneRange: ' + str(self.toneRange_) + '\n\t' + \
            super().__repr__().replace('\n','\n\t')
            

class Invertable(VTable):    
    def __init__(self,name, plusPole, minusPole):
        VTable.__init__(self,name,plusPole, minusPole)
        self.invert_ = CurrentNextable()

    def invert(self,level):
        self.invert_.update(level)

    def x(self):
        self.invert_.x()
        super().x()

    def __repr__(self):
        return 'Invertable: ' + self.name + '\n\t' + \
            'invert: ' + str(self.invert_) + '\n\t' +\
            super().__repr__().replace('\n','\n\t')

        
