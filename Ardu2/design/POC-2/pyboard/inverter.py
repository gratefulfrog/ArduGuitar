#!/usr/bin/python3

from state import *
from dictMgr import *

currentConfig = [0 for x in range(13)]
nextConfig    = currentConfig

def baseFunc(onOff,name,att,val):
    """ special case for turning off, no settings!
    """    
    setting = None
    # if onOff is True, were are making a setting
    if onOff:
        setting = (shiftRegDict[name][att][val])
    masking = maskingDict[name][att]
    return (setting,masking)

def funcer(name, att, state):
    """ To call funcer:
    >>> funcer('A',State.Inverter,State.Inverter.on)
    """
    # special case for the inverter, it can be off, ie None !
    onOff = not state == State.Inverter.off
    
    (setting, masking) = baseFunc(onOff,
                                  name,
                                  att,
                                  state)
    doSettingMasking(setting,masking)
    
def doSettingMasking(setting,masking):
    for (reg,mask) in masking:
        print("masking: ", "{0:d}".format(reg), "{0:#b}".format(mask))
        nextConfig[reg] &= mask
    if setting:
        nextConfig[setting[0]] |= pow(2,setting[1])
    print ('setting: ', setting)
    print(["{0:#b}".format(x) for x in nextConfig])


######
######

# this is just junk to be removed and replaced by a coil-master class!

class Inverter:
    def __init__(self, name, setFunc, initialState=State.Inverter.off):
        self.name = name
        self.setFunc = setFunc
        self.state = initialState
        self.setFunc(self.name, initialState)

    def setState(self, state):
        """update internal state and call stateFunc on it
        """
        self.state = state
        self.setFunc(state)

    def __repr__(self):
        return 'Inverter:\n\tstate: ' + \
            str(self.state) + '\n\tsetFunc: ' + str(self.setFunc)
    
