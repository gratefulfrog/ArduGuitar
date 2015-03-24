#!/usr/bin/python3
# app.py
# provides classes for the application level
# 

#from state import theState
#from bitMgr import bitMgr,BitMgr

from components import *
from state import State

class App():
    def __init__(self):
        self.coils = []
        for coil in State.coils[:-1]:
            self.coils += [Invertable(coil),]
        self.coils += [VTable(State.coils[-1]),]

