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
    plus = 'p'
    minus = 'm'

    def __init__(self, name):
        self.name = name
        self.plusConnected2 = CurrentNextable()
        self.minusConnected2 = CurrentNextable()

    def connect(self, myPole, otherPole):
        if myPole == self.plus:
            self.plusConnected2.update(otherPole)
        else:
            self.minusConnected2.update(otherPole)
    
    def x(self):
        self.plusConnected2.x() 
        self.minusConnected2.x()

    def __repr__(self):
        return 'Connectable: ' + self.name + '\n\t' + \
            self.plus   + ': ' + str(self.plusConnected2) + '\n\t' +\
            self.minus  + ': ' + str(self.minusConnected2) 

class VTable(Connectable):
    
    def __init__(self,name):
        Connectable.__init__(self,name)
        self.vol = CurrentNextable()
        self.tone  = CurrentNextable()

    def vol(self,level):
        self.vol.update(level)

    def tone(self,level):
        self.tone.update(level)

    def x(self):
        self.vol.x()
        self.tone.x()

    def __repr__(self):
        return 'VTable: ' + self.name + '\n\t' + \
            'vol: ' + str(self.vol) + '\n\t' +\
            'tone: ' + str(self.tone) + '\n\t' + \
            super().__repr__().replace('\n','\n\t')
            

        
