#!/usr/bin/python3
# ivt-control.py
# provides functionality to update Inverter, Volume, Tone & ToneRange

 
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

def updateNextConfig(name, att, state):
    """ To call funcer:
    >>> updateNextConfig('A',State.Inverter,State.l2)
    """
    # all states can be 'off', ie None !
    onOff = not state == State.off
    
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
