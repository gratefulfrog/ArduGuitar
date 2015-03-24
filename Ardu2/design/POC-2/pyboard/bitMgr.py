#!/usr/bin/python3
# bitMgr.py
# provides functionality to update bit arrays for shifting
 
from state import State
from dictMgr import *

nbShiftRegs = 13  # i.e. on [0,13[
nbSwitchRegs = 4
connectionUpdateOnly = 1010

class BitMgr:
    cur = 0
    nex = 1
    switchRegEndPoints = (0,nbSwitchRegs)
    ivtrRegEndPoints = (nbSwitchRegs,nbShiftRegs)
    allRegEndPoints = (0,nbShiftRegs)

    def baseFunc(onOff,name,att,val):
        """ special case for turning off, no settings!
        """    
        setting = None
        # if onOff is True, were are making a setting
        if onOff:
            setting = (vtrDict[name][att][val])
        masking = maskingDict[name][att]
        return (setting,masking)

    def __init__(self,nb_shiftRegs=nbShiftRegs):
        self.cnConfig = ([0 for x in range(BitMgr.allRegEndPoints[0],
                                           BitMgr.allRegEndPoints[1])], 
                         [0 for x in range(BitMgr.allRegEndPoints[0],
                                           BitMgr.allRegEndPoints[1])])

    def reset(self,whatRange, curBool=True,nexBool=True):
        cnRange = []
        if curBool:
            cnRange += [BitMgr.cur]
        if nexBool:
            cnRange += [BitMgr.nex]
        for i in cnRange:
            for j in range(whatRange[0],whatRange[1]):
                self.cnConfig[i][j] = 0

    def current(self):
        return self.cnConfig[BitMgr.cur]

    def next(self):
        return self.cnConfig[BitMgr.nex]

    def update(self,name, att, state=connectionUpdateOnly):
        """ To call update(...) on name, att, state
        >>> update('A',State.Inverter,State.l2)
        To call update(...) on connections
        >>> update(('A',0),('B',1))
        """
        if state == connectionUpdateOnly:
            self.doSettingMasking(connectionsDict[(name,att)],[])
        else:
            # all states can be 'off', ie None !
            onOff = not state == State.off
            (setting, masking) = BitMgr.baseFunc(onOff,
                                                 name,
                                                 att,
                                                 state)
            self.doSettingMasking(setting,masking)
        
    def x(self):
        for i in range(len(self.cnConfig[BitMgr.nex])):
            self.cnConfig[BitMgr.cur][i] = self.cnConfig[BitMgr.nex][i]
        self.printConfigs(None,[])
        
    def doSettingMasking(self,setting,masking):
        for (reg,mask) in masking:
            self.cnConfig[BitMgr.nex][reg] &= mask
        if setting:
            self.cnConfig[BitMgr.nex][setting[0]] |= pow(2,setting[1])
        self.printConfigs(setting,masking)

    def printConfigs(self,setting,masking):
        for (reg,mask) in masking:
            print("masking: ", ["{0:d}".format(reg), "{0:#b}".format(mask)])
        print('setting: ' + str(setting))
        print(self)
        """
        print('currentConfig:\t' + \
                  str(["{0:#b}".format(x) \
                           for x in self.cnConfig[BitMgr.cur]]))
        print('nextConfig:\t' + \
                  str(["{0:#b}".format(x) \
                           for x in self.cnConfig[BitMgr.nex]]))
        """

    def __repr__(self):
        s = 'currentConfig:\t' + \
            str(["{0:#b}".format(x) \
                     for x in self.cnConfig[BitMgr.cur]]) + '\n' + \
                     'nextConfig:\t' + \
                     str(["{0:#b}".format(x) \
                              for x in self.cnConfig[BitMgr.nex]])
        return s


