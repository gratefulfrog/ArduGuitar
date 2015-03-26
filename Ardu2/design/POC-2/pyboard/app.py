#!/usr/local/bin/python3.4
# app.py
# provides classes for the application level
# 

from bitMgr import BitMgr
from components import Invertable,VTable
from state import State
from spiMgr import SPIMgr

class App():
    sets  = [Invertable.invert,
             VTable.vol,
             VTable.tone,
             VTable.toneRange]
    
    def stateNeg2SetIndex(stateNeg):
        return abs(stateNeg)-1
    
    def __init__(self):
        self.bitMgr = BitMgr()
        self.state = State()
        self.coils = {}
        self.resetConnections = True
        for coil in State.coils[:-1]:
            self.coils[coil] = Invertable(coil)
        self.coils[State.coils[-1]]= VTable(State.coils[-1])
        self.spiMgr = SPIMgr(State.spiOnX,State.spiLatchPinName)
        # turn all off
        self.spiMgr.update(self.bitMgr.cnConfig[0])

    def set(self,name,att,state):
        App.sets[App.stateNeg2SetIndex(att)](self.coils[name],state)
        self.bitMgr.update(name,att,state)

    def connect(self,name,pole,otherName,otherPole):
        if not self.resetConnections:
            self.bitMgr.reset(BitMgr.switchRegEndPoints, 
                              curBool=False,
                              nexBool=True)
            self.resetConnections = True
        self.coils[name].connect(pole,(otherName,otherPole))
        self.bitMgr.update((name,pole),
                           (otherName,otherPole))

    def x(self):
        for coil in self.coils.values():
            coil.x()
        self.bitMgr.x()
        #send bits!
        self.spiMgr.update(self.bitMgr.cnConfig[0])
        self.resetConnections = False




