#!/usr/bin/python3
# components/py
# provides classes for all physical components of the guitar
# 

from state import theState
from ivtControl import ivtControl

class CurrentNextable:
    cur = 0
    nex = 1

    def __init__(self):
        self.cn = [theState.off,theState.off]
    
    def current(self):
        return self.cn[self.cur]

    def next(self):
        return self.cn[self.nex]

    def update(self, new):
        self.cn[self.nex] = new

    def x(self):
        self.cn[self.cur] = self.cn[self.nex]

    def __repr__(self):
        return 'CurrentNextable: ' +  \
            str(self.cn)

class Connectable:
    def __init__(self, name):
        self.name = name
        self.connected2 = [CurrentNextable(),CurrentNextable()]

    def connect(self, myPoleId, coilPolePair):
        self.connected2[myPoleId].update(coilPolePair)    
    
    def x(self):
        for c in self.connected2:
            if (not c == None):
                c.x() 

    def __repr__(self):
        return 'Connectable: ' + self.name + '\n\t' + \
            'Connected2: ' + str(self.connected2)

class VTable(Connectable):    
    def __init__(self,name):
        Connectable.__init__(self,name)
        self.vol_ = CurrentNextable()
        self.tone_  = CurrentNextable()
        self.toneRange_  = CurrentNextable()

    def vol(self,level):
        self.vol_.update(level)
        ivtControl.update(self.name,theState.Vol,level)

    def tone(self,level):
        self.tone_.update(level)
        ivtControl.update(self.name,theState.Tone,level)

    def toneRange(self,level):
        self.toneRange_.update(level)
        ivtControl.update(self.name,theState.ToneRange,level)

    def x(self):
        self.vol_.x()
        self.tone_.x()
        self.toneRange_.x()
        super().x()
        ivtControl.x()

    def __repr__(self):
        return 'VTable: ' + self.name + '\n\t' + \
            'vol: ' + str(self.vol_) + '\n\t' +\
            'tone: ' + str(self.tone_) + '\n\t' + \
            'toneRange: ' + str(self.toneRange_) + '\n\t' + \
            super().__repr__().replace('\n','\n\t')
            

class Invertable(VTable):    
    def __init__(self,name):
        VTable.__init__(self,name)
        self.invert_ = CurrentNextable()

    def invert(self,level):
        self.invert_.update(level)
        ivtControl.update(self.name,theState.Inverter,level)

    def x(self):
        self.invert_.x()
        super().x()

    def __repr__(self):
        return 'Invertable: ' + self.name + '\n\t' + \
            'invert: ' + str(self.invert_) + '\n\t' +\
            super().__repr__().replace('\n','\n\t')

        
