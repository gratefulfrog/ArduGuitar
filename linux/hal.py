#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
hal.py
This is it takes abstract commands like:
* set the volume to 5, 
* set the tone to 3, 
* turn on neck pickup,
* turn split
* etc
and sends them to the protocol object as pin,value pairs
"""

import sys 
import config
import protocol

class Hal():
    """ 
    Hardware Abstraction Layer: Provides abstract interface to the Arduino, 
    translates model values into hardware settings.
    """
    # incoming data formats to be moved to config

    def __init__(self,arduGuitarConf,comm=True):        
        # com argument is to allow execution without a bluetooth connection
        # creat a instance with a conf and a Protocol object instance
        self.conf = arduGuitarConf
        # get a Protocol object instance
        self.protocol = protocol.Protocol(arduGuitarConf,comm)
        print("hal created!")

    def ok(self):
        # this asks the protocol to check the hardware-heartbeat
        # no return if all is ok,
        # the protocol will raise an exception if not
        self.protocol.heartbeatCheck()

    def update(self, argDict):
        """
        for any of the dict keys that are not none, make the corresponding
        (pin,value) tuple,
        send a list of those tuples to the protocol
        """
        print("called hal.update")
        outgoingTupleLis = []
        for key in argDict.keys():
            if argDict[key] != None: 
                outgoingTupleLis += self.buildTuples(key,argDict[key])
        print outgoingTupleLis
        self.protocol.send(outgoingTupleLis)

    def buildTuples(self,key,val):
        # returns some tuples depending on the key argument
        #print str(key) + ": " +str(val)
        res = []
        # first, are we dealing with volume?
        if key == self.conf.vocab.volKey:
            # then get the corresponding 2 pins and values from conf
            res.append((self.conf.hal.volPins[0],
                        self.conf.hal.volPWM[0][int((round(val/self.conf.hal.vtDiviser)))]))
            res.append((self.conf.hal.volPins[1],
                        self.conf.hal.volPWM[1][int((round(val/self.conf.hal.vtDiviser)))]))
            res.append((self.conf.hal.volPins[2],
                        self.conf.hal.volPWM[2][int((round(val/self.conf.hal.vtDiviser)))]))
        # if not, is it tone?
        elif key == self.conf.vocab.toneKey:
            # then get the value from conf
            res.append((self.conf.hal.tonePin,
                        self.conf.hal.tonePWM[int((round(val/self.conf.hal.vtDiviser)))]))
        # otherwise it's a pickup or switch
        else: 
            # get value from conf
            res.append((self.conf.hal.pickup2PinDict[key],self.conf.hal.onOff2ValDict[val]))
        return res


def main():
    conf = config.ArduGuitarConf()
    hal = Hal(conf) 
    while(True):
        s = raw_input("update line (att=val,separated by commas, eg vol=10,bridge=True): ")
        tl = eval('hal.update(' + s +')')
        hal.ok()

    
if __name__ == '__main__':
    main()
