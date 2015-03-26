#!/usr/local/bin/python3.4
# pyb.py for off-pyboard testing

class SPI():
    MASTER = 'Master'
    SLAVE = 'Slave'

    def __init__(self,side,MasterOrSlave):
        self.side = side
        self.MoS = MasterOrSlave 

    def send(self,bits):
        print("send:\t{0:#b}".format(bits))
        
    def __repr__(self):
        return 'SPI:' + \
            '\n\tBoardSide:\t' + str(self.side) + \
            '\n\tMasterOrSlave:\t' + str(self.MoS)

class Pin():
    OUT_PP = 'OUT_PP'

    def __init__(self, latch, po):
        self.latchPin = latch
        self.pinOut = po
        self.value = 0

    def high(self):
        self.value = 1
        print (str(self) + '\n\tset: HIGH')

    def low(self):
        self.value = 0
        print (str(self) + '\n\tset: LOW')

    def __repr__(self):
        return 'Pin:' + \
            '\n\tLatchPin:\t' + str(self.latchPin) + \
            '\n\tPinOut:\t' + str(self.pinOut) + \
            '\n\tValue:\t' + str(self.value) 
