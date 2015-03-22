#!/usr/bin/python3
# ivt-control.py
# provides functionality to update Inverter, Volume, Tone & ToneRange
 
from state import theState
from dictMgr import *

class IVTControl:
    cur = 0
    nex = 1

    def baseFunc(onOff,name,att,val):
        """ special case for turning off, no settings!
        """    
        setting = None
        # if onOff is True, were are making a setting
        if onOff:
            setting = (shiftRegDict[name][att][val])
        masking = maskingDict[name][att]
        return (setting,masking)

    def __init__(self,nb_shiftRegs=13):
        self.cnConfig = ([0 for x in range(nb_shiftRegs)], 
                         [0 for x in range(nb_shiftRegs)])

    def current(self):
        return self.cnConfig[ivtControl.cur]

    def next(self):
        return self.cnConfig[ivtControl.nex]

    def update(self,name, att, state):
        """ To call updateNextConfig:
        >>> updateNextConfig('A',theState.Inverter,theState.l2)
        """
        # all states can be 'off', ie None !
        onOff = not state == theState.off
        
        (setting, masking) = IVTControl.baseFunc(onOff,
                                                 name,
                                                 att,
                                                 state)
        self.doSettingMasking(setting,masking)
        
    def x(self):
        for i in range(len(self.cnConfig[IVTControl.nex])):
            self.cnConfig[IVTControl.cur][i] = self.cnConfig[IVTControl.nex][i]
        self.printConfigs(None,[])
        
    def doSettingMasking(self,setting,masking):
        for (reg,mask) in masking:
            self.cnConfig[IVTControl.nex][reg] &= mask
        if setting:
            self.cnConfig[IVTControl.nex][setting[0]] |= pow(2,setting[1])
        self.printConfigs(setting,masking)

    def printConfigs(self,setting,masking):
        for (reg,mask) in masking:
            print("masking: ", ["{0:d}".format(reg), "{0:#b}".format(mask)])
        print('setting: ' + str(setting))
        print('currentConfig:\t' + \
                  str(["{0:#b}".format(x) \
                           for x in self.cnConfig[IVTControl.cur]]))
        print('nextConfig:\t' + \
                  str(["{0:#b}".format(x) \
                           for x in self.cnConfig[IVTControl.nex]]))

ivtControl =  IVTControl()
